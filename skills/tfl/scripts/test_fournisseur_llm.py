#!/usr/bin/env python3
"""Générer le rapport TFL : OpenCode Go, catalogue général OpenCode, OpenRouter."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import signal
import uuid
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

API_URL = "https://opencode.ai/zen/go/v1/models"
OPENCODE_API_URL = "https://opencode.ai/zen/v1/models"
OPENCODE_SOURCE_URL = "https://opencode.ai/v2/docs/console/models/"
SOURCE_URL = "https://opencode.ai/docs/go/"
CONTEXT_METADATA_URL = "https://models.dev/api.json"
ROOT = Path(__file__).resolve().parent.parent
_PERFORMANCE_SPEC = importlib.util.spec_from_file_location('tfl_performance', Path(__file__).with_name('performance.py'))
performance = importlib.util.module_from_spec(_PERFORMANCE_SPEC)
_PERFORMANCE_SPEC.loader.exec_module(performance)
_BLACKLIST_SPEC = importlib.util.spec_from_file_location('tfl_blacklist', Path(__file__).with_name('model_blacklist.py'))
blacklist = importlib.util.module_from_spec(_BLACKLIST_SPEC)
_BLACKLIST_SPEC.loader.exec_module(blacklist)

MIN_CONTEXT_TOKENS = 1_000_000
MAX_REFERENCE_AVERAGE_USD_PER_MILLION = 0.5
BLACKLISTED_MODEL_IDS = {"muse-spark-1.2-contributor"}
NON_TEXT_OUTPUT_MODALITIES = {"audio", "video", "speech", "sound"}
GO_PROTOCOL_PATHS = {"responses": "responses", "chat_completions": "chat/completions", "messages": "messages"}
# Contrats de transport des SDK publiés, indépendants des identifiants de modèles.
GO_SDK_PROTOCOLS = {
    "@ai-sdk/openai-compatible": ("chat_completions", "https://ai-sdk.dev/providers/openai-compatible-providers"),
    "@ai-sdk/openai": ("responses", "https://github.com/vercel/ai/blob/main/packages/openai/src/openai-provider.ts"),
    "@ai-sdk/anthropic": ("messages", "https://ai-sdk.dev/providers/ai-sdk-providers/anthropic"),
}
POLICIES = {
    "mode1": "anthony.demard44@gmail.com",
    "mode2": "az.github@pixs.fr",
}

class PricingTables(HTMLParser):
    """Extraire les cellules sans les anciens montants barrés."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.struck = 0
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "table":
            if self.table is not None:
                raise RuntimeError("tableaux tarifaires OpenCode imbriqués non reconnus")
            self.table = []
        elif self.table is not None:
            if tag == "tr":
                if self.row is not None:
                    raise RuntimeError("lignes tarifaires OpenCode mal formées")
                self.row = []
            elif tag in ("td", "th"):
                if self.cell is not None or self.row is None:
                    raise RuntimeError("cellules tarifaires OpenCode mal formées")
                self.cell = []
            elif tag in ("del", "s", "strike"):
                self.struck += 1
            elif tag == "br" and self.cell is not None:
                self.cell.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.struck:
            self.text.append(data)
        if self.cell is not None and not self.struck:
            self.cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.table is None:
            return
        if tag in ("del", "s", "strike"):
            self.struck = max(0, self.struck - 1)
        elif tag in ("td", "th") and self.cell is not None:
            if self.row is None:
                raise RuntimeError("cellule tarifaire OpenCode hors ligne")
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table":
            self.tables.append(self.table)
            self.table = None


def pricing_name(value: str) -> str:
    """Comparer uniquement la casse et les séparateurs des noms publiés."""
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def go_price(value: str, *, optional: bool = False) -> float | None:
    if optional and value in ("-", "—", ""):
        return None
    if value.casefold() == "free":
        return 0.0
    if not re.fullmatch(r"\$(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", value):
        raise RuntimeError("montant tarifaire OpenCode non reconnu")
    try:
        number = float(Decimal(value[1:].replace(",", "")))
    except (InvalidOperation, ValueError, OverflowError) as exc:
        raise RuntimeError("montant tarifaire OpenCode invalide") from exc
    if not math.isfinite(number) or number < 0:
        raise RuntimeError("montant tarifaire OpenCode non fini ou négatif")
    return number


def go_variant(label: str) -> tuple[str, str, str | None]:
    match = re.fullmatch(r"([^()]+?)(?:\s*\(([^()]*)\))?", label)
    if match is None:
        raise RuntimeError("libellé tarifaire OpenCode non reconnu")
    name, qualifier = match.groups()
    qualifier = qualifier.strip() if qualifier else None
    period = "standard"
    if qualifier and re.fullmatch(r"off[ -]?peak", qualifier, re.I):
        period = "off_peak"
    elif qualifier and qualifier.casefold() == "peak":
        period = "peak"
    elif qualifier and not re.fullmatch(
        r"(?:[<>]=?|[≤≥])\s*\d+(?:\.\d+)?[KM]?\s+tokens|\d+(?:\.\d+)?%\s+off",
        qualifier, re.I,
    ):
        raise RuntimeError("variante tarifaire OpenCode non reconnue")
    return name.strip(), period, qualifier


def parse_go_pricing(document: str) -> dict:
    parser = PricingTables()
    parser.feed(document)
    parser.close()
    if parser.table is not None or parser.row is not None or parser.cell is not None:
        raise RuntimeError("tableau tarifaire OpenCode incomplet")
    if not re.search(r"\bprices?\s+(?:are\s+)?per\s+(?:1\s*m|1,?000,?000)\s+tokens\b",
                     " ".join(parser.text), re.I):
        raise RuntimeError("unité tarifaire OpenCode non vérifiable : 1M tokens requis")
    references: dict[str, dict] = {}
    table_count = 0
    for table in parser.tables:
        if not table:
            continue
        headers = [pricing_name(cell) for cell in table[0]]
        if not {"model", "input", "output"}.issubset(headers):
            continue
        if len(headers) != len(set(headers)):
            raise RuntimeError("colonnes tarifaires OpenCode ambiguës")
        table_count += 1
        for cells in table[1:]:
            if len(cells) != len(headers):
                raise RuntimeError("ligne tarifaire OpenCode incomplète")
            values = dict(zip(headers, cells))
            name, period, qualifier = go_variant(values["model"])
            key = pricing_name(name)
            if not key:
                raise RuntimeError("nom tarifaire OpenCode vide")
            variant = {
                "label": values["model"], "period": period, "qualifier": qualifier,
                "input": go_price(values["input"]),
                "output": go_price(values["output"]),
                "cache_read": go_price(values.get("cachedread", ""), optional=True),
                "cache_write": go_price(values.get("cachedwrite", ""), optional=True),
            }
            if not math.isfinite((variant["input"] + variant["output"]) / 2):
                raise RuntimeError("coût moyen OpenCode non fini")
            entry = references.setdefault(key, {"name": name, "variants": []})
            if entry["name"].casefold() != name.casefold():
                raise RuntimeError("correspondance tarifaire OpenCode ambiguë")
            previous = next((v for v in entry["variants"]
                             if v["period"] == period and v["qualifier"] == qualifier), None)
            if previous is not None and previous != variant:
                raise RuntimeError("tarifs OpenCode contradictoires pour " + name)
            if previous is None:
                entry["variants"].append(variant)
    if not table_count or not references:
        raise RuntimeError("aucun tableau tarifaire OpenCode reconnu")
    return references


def fetch_catalog_pricing(source_url: str, timeout: float) -> dict:
    request = Request(source_url, headers={"Accept": "text/html", "User-Agent": "TFL/1.0"})
    maximum_bytes = 2 * 1024 * 1024
    with urlopen(request, timeout=timeout) as response:
        raw = response.read(maximum_bytes + 1)
        source = response.geturl()
    if len(raw) > maximum_bytes:
        raise RuntimeError("documentation tarifaire OpenCode trop volumineuse")
    try:
        document = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("documentation tarifaire OpenCode non UTF-8") from exc
    return {
        "source": source, "retrieved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "currency": "USD", "unit": "per_million_tokens",
        "selection_rule": "maximum_average_off_peak_context_tier",
        "sha256": hashlib.sha256(raw).hexdigest(), "models": parse_go_pricing(document),
    }


def fetch_go_pricing(timeout: float) -> dict:
    return fetch_catalog_pricing(SOURCE_URL, timeout)


def fetch_opencode_pricing(timeout: float) -> dict:
    result = fetch_catalog_pricing(OPENCODE_SOURCE_URL, timeout)
    result["selection_rule"] = "maximum_average_published_context_tier"
    return result


def go_reference(model: dict, pricing: dict) -> dict | None:
    candidates = {pricing_name(value) for value in (model.get("id"), model.get("name"))
                  if isinstance(value, str) and pricing_name(value) in pricing["models"]}
    if len(candidates) > 1:
        raise RuntimeError("correspondance tarifaire Go ambiguë pour " + model["id"])
    return pricing["models"][next(iter(candidates))] if candidates else None


def go_reference_prices(reference: dict) -> dict | None:
    variants = reference["variants"]
    off_peak = [v for v in variants if v["period"] == "off_peak"]
    if not off_peak:
        off_peak = [v for v in variants if v["period"] == "standard"]
    if not off_peak:
        return None
    selected = max(off_peak, key=lambda v: (v["input"] + v["output"]) / 2)
    prices = {
        "input_off_peak": selected["input"], "output_off_peak": selected["output"],
        "average_off_peak": (selected["input"] + selected["output"]) / 2,
        "cache_read_off_peak": selected["cache_read"],
        "cache_write_off_peak": selected["cache_write"],
        "selected_variant": selected["label"],
    }
    peak = [v for v in variants if v["period"] == "peak"]
    if peak:
        selected_peak = max(peak, key=lambda v: (v["input"] + v["output"]) / 2)
        prices.update({
            "input_peak": selected_peak["input"], "output_peak": selected_peak["output"],
            "average_peak": (selected_peak["input"] + selected_peak["output"]) / 2,
            "cache_read_peak": selected_peak["cache_read"],
            "cache_write_peak": selected_peak["cache_write"],
        })
    return prices


def opencode_reference_prices(reference: dict) -> dict:
    selected = max(reference["variants"], key=lambda v: (v["input"] + v["output"]) / 2)
    return {"input": selected["input"], "output": selected["output"],
            "average": (selected["input"] + selected["output"]) / 2,
            "cache_read": selected["cache_read"], "cache_write": selected["cache_write"],
            "selected_variant": selected["label"]}


def money(value: float | None) -> str:
    if value is None:
        return "—"
    return f"${value:.4f}".rstrip("0").rstrip(".")


def cost_color(value: float | None) -> str:
    if value is None:
        return "⚪"
    if value <= 0.2:
        return "🟢"
    if value <= 0.4:
        return "🟡"
    if value <= 0.5:
        return "🟠"
    return "🔴"


def escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", nargs="?", choices=("auto", "mode1", "mode2"), default=None)
    parser.add_argument("--policy", dest="policy_option", choices=("auto", "mode1", "mode2"), default=None)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def secret_for(policy: str) -> str:
    account = POLICIES[policy]
    result = subprocess.run(
        ["secret-tool", "lookup", "service", "pllm", "policy", policy,
         "provider", "opencodego", "account", account],
        capture_output=True,
        timeout=15,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("clé API inaccessible pour " + policy)
    return result.stdout.decode().strip()


def select_secret(requested: str) -> tuple[str, str]:
    policies = ("mode1", "mode2") if requested == "auto" else (requested,)
    errors = []
    for policy in policies:
        try:
            return policy, secret_for(policy)
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError("; ".join(errors))


def fetch_models(api_key: str, timeout: float) -> dict:
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + api_key,
        "User-Agent": "TOCG/1.0",
    }
    with urlopen(Request(API_URL, headers=headers), timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise RuntimeError("réponse /models invalide")
    payload["retrieved_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return payload


def fetch_opencode_models(timeout: float) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "TFL/1.0"}
    with urlopen(Request(OPENCODE_API_URL, headers=headers), timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise RuntimeError("réponse du catalogue général OpenCode invalide")
    payload["retrieved_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return payload


def fetch_catalog_metadata(provider_id: str, models_api: str, timeout: float) -> dict:
    '''Récupérer contexte, modalités et transport du catalogue OpenCode demandé.'''
    headers = {
        "Accept": "application/json",
        "User-Agent": "TOCG/1.0",
    }
    with urlopen(Request(CONTEXT_METADATA_URL, headers=headers), timeout=timeout) as response:
        payload = json.load(response)
    provider = payload.get(provider_id) if isinstance(payload, dict) else None
    models = provider.get("models") if isinstance(provider, dict) else None
    if not isinstance(models, dict):
        raise RuntimeError("métadonnées de catalogue OpenCode invalides")
    return {
        "source": CONTEXT_METADATA_URL,
        "provider_id": provider_id, "models_api": models_api,
        "retrieved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "provider": {key: provider[key] for key in ("api", "npm", "api_protocol") if key in provider},
        "models": models,
    }


def fetch_go_metadata(timeout: float) -> dict:
    return fetch_catalog_metadata("opencode-go", API_URL, timeout)


def fetch_opencode_metadata(timeout: float) -> dict:
    return fetch_catalog_metadata("opencode", OPENCODE_API_URL, timeout)




def go_model_metadata(model: dict, metadata: dict) -> dict:
    models = metadata.get("models", {})
    if not isinstance(models, dict):
        raise RuntimeError("catalogue de métadonnées OpenCode invalide")
    record = models.get(model.get("id"), {})
    if not isinstance(record, dict):
        raise RuntimeError("métadonnées du modèle OpenCode invalides")
    return record


def declared_modalities(record: dict, direction: str) -> list[str] | None:
    declarations = [record.get(direction + "_modalities"), record.get(direction + "Modalities")]
    for container, key in (("architecture", direction + "_modalities"), ("modalities", direction)):
        value = record.get(container)
        if value is not None:
            if not isinstance(value, dict):
                raise RuntimeError("déclaration de modalités OpenCode invalide")
            declarations.append(value.get(key))
    known = []
    for values in declarations:
        if values is None:
            continue
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            raise RuntimeError("liste de modalités OpenCode invalide")
        if values:
            known.append(sorted({value.strip().lower() for value in values}))
    if known and any(value != known[0] for value in known[1:]):
        raise RuntimeError("modalités OpenCode contradictoires")
    return known[0] if known else None


def go_modalities(model: dict, metadata: dict, api_retrieved_at: str | None) -> dict:
    reference = go_model_metadata(model, metadata)
    result = {"modalities_metadata": {}}
    api_source = "opencode-api" if metadata.get("provider_id") == "opencode" else "opencode-go-api"
    for direction in ("input", "output"):
        api_values = declared_modalities(model, direction)
        metadata_values = declared_modalities(reference, direction)
        if api_values is not None and metadata_values is not None and api_values != metadata_values:
            raise RuntimeError("modalités OpenCode contradictoires entre API et models.dev")
        values = api_values if api_values is not None else metadata_values
        result[direction + "_modalities"] = values
        result["modalities_metadata"][direction] = {
            "source": api_source if api_values is not None else "models.dev" if values is not None else None,
            "source_api": metadata.get("models_api", API_URL) if api_values is not None else CONTEXT_METADATA_URL if values is not None else None,
            "retrieved_at": api_retrieved_at if api_values is not None else metadata.get("retrieved_at") if values is not None else None,
        }
    return result


def safe_go_url(value: object) -> str:
    if not isinstance(value, str) or not value or any(c.isspace() for c in value) or any(c in value for c in ("\\", "?", "#")):
        raise RuntimeError("URL de routage OpenCode non sûre")
    try:
        parsed = urlsplit(value)
        safe = (parsed.scheme == "https" and parsed.hostname == urlsplit(API_URL).hostname
                and parsed.port in (None, 443) and parsed.username is None and parsed.password is None
                and not parsed.query and not parsed.fragment)
    except ValueError as exc:
        raise RuntimeError("URL de routage OpenCode invalide") from exc
    if not safe:
        raise RuntimeError("origine de routage OpenCode non sûre")
    return value.rstrip("/")


def go_transport(model: dict, metadata: dict, api_retrieved_at: str | None) -> dict:
    endpoint, protocol = model.get("api_endpoint"), model.get("api_protocol")
    explicit_api = endpoint is not None or protocol is not None
    api_source = "opencode-api" if metadata.get("provider_id") == "opencode" else "opencode-go-api"
    source = api_source if explicit_api else "models.dev"
    details = {
        "source_api": metadata.get("models_api", API_URL) if explicit_api else CONTEXT_METADATA_URL,
        "retrieved_at": api_retrieved_at if explicit_api else metadata.get("retrieved_at"),
        "generation_tested": False,
    }
    result = {"api_endpoint": None, "api_protocol": None, "endpoint_source": source,
              "routing_status": "not_verified", "routing_warning": None, "routing_metadata": details}
    if explicit_api:
        endpoint = safe_go_url(endpoint) if endpoint is not None else None
        if endpoint is None or protocol is None:
            result["routing_warning"] = "route explicite OpenCode incomplète"
            return result
        if not isinstance(protocol, str) or protocol not in GO_PROTOCOL_PATHS:
            result["routing_warning"] = "protocole explicite OpenCode non reconnu"
            return result
        if not urlsplit(endpoint).path.endswith("/" + GO_PROTOCOL_PATHS[protocol]):
            raise RuntimeError("endpoint OpenCode incompatible avec le protocole déclaré")
    else:
        provider = metadata.get("provider", {})
        if model.get("id") not in metadata.get("models", {}):
            result["routing_warning"] = "modèle absent des métadonnées de transport OpenCode"
            return result
        override = go_model_metadata(model, metadata).get("provider")
        if not isinstance(provider, dict) or (override is not None and not isinstance(override, dict)):
            raise RuntimeError("métadonnées de transport OpenCode invalides")
        override = override or {}
        effective = {**provider, **override}
        base = effective.get("api")
        base = safe_go_url(base) if base is not None else None
        sdk = effective.get("npm")
        if sdk is not None and not isinstance(sdk, str):
            raise RuntimeError("SDK de transport OpenCode invalide")
        details.update({"sdk": sdk, "api_base": base,
                        "sdk_scope": "model" if "npm" in override else "provider",
                        "api_scope": "model" if "api" in override else "provider"})
        protocol = effective.get("api_protocol")
        if protocol is None:
            contract = GO_SDK_PROTOCOLS.get(sdk)
            if contract is not None:
                protocol, reference = contract
                details["protocol_reference"] = reference
        else:
            details["protocol_reference"] = "declared_api_protocol"
        if not isinstance(protocol, str) or protocol not in GO_PROTOCOL_PATHS:
            result["routing_warning"] = "protocole ou SDK OpenCode absent ou non reconnu"
            return result
        if base is None:
            result["routing_warning"] = "base API OpenCode absente"
            return result
        endpoint = base + "/" + GO_PROTOCOL_PATHS[protocol]
    result.update({"api_endpoint": endpoint, "api_protocol": protocol,
                   "routing_status": "documented", "routing_warning": None})
    return result


def positive_integer(value: object) -> int | None:
    try:
        parsed = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def context_info(model: dict, metadata: dict) -> tuple[int | None, str | None]:
    '''Retourner le contexte vérifié et sa source, sans inventer de capacité.'''
    for key in ("context_length", "contextLength"):
        value = positive_integer(model.get(key))
        if value is not None:
            return value, "api"
    reference = go_model_metadata(model, metadata)
    if isinstance(reference, dict):
        limit = reference.get("limit")
        if isinstance(limit, dict):
            value = positive_integer(limit.get("context"))
            if value is not None:
                return value, "models.dev"
        for key in ("context_length", "contextLength"):
            value = positive_integer(reference.get(key))
            if value is not None:
                return value, "models.dev"
    return None, None


def context_label(tokens: int | None) -> str:
    if tokens is None:
        return "Non vérifié"
    if tokens >= 1_000_000:
        return f"{tokens / 1_000_000:.3g}M"
    if tokens >= 1_000:
        return f"{tokens / 1_000:.3g}K"
    return str(tokens)


def build_rows(payload: dict, metadata: dict, pricing: dict, *, general_catalog: bool = False, blacklisted_models: tuple[str, ...] | None = None) -> tuple[list[dict], list[dict]]:
    blacklisted_models = blacklist.load_models() if blacklisted_models is None else blacklisted_models
    if general_catalog and metadata.get("provider_id") != "opencode":
        raise RuntimeError("métadonnées du catalogue général OpenCode : fournisseur incorrect")
    known = []
    excluded = []
    matched_names: dict[str, str] = {}
    for model in payload["data"]:
        if not isinstance(model, dict) or not model.get("id"):
            continue
        model_id = model["id"]
        if blacklist.is_blocked(model_id, blacklisted_models):
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "reason": "blacklist permanente" if model_id in BLACKLISTED_MODEL_IDS else "liste noire LM",
            })
            continue
        context, context_source = context_info(model, metadata)
        if context is None or context < MIN_CONTEXT_TOKENS:
            reason = (
                "contexte non vérifiable; seuil obligatoire de 1M"
                if context is None
                else f"contexte {context} tokens inférieur au seuil obligatoire de 1M"
            )
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "context_length": context,
                "reason": reason,
            })
            continue
        modality_info = go_modalities(model, metadata, payload.get("retrieved_at"))
        modalities = modality_info["output_modalities"]
        non_text = sorted(set(modalities or []) & NON_TEXT_OUTPUT_MODALITIES)
        if non_text:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "output_modalities": modalities,
                "reason": "sortie audio/vidéo exclue",
            })
            continue
        reference = go_reference(model, pricing)
        prices = (opencode_reference_prices(reference) if general_catalog else go_reference_prices(reference)) if reference else None
        if prices is None:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "context_length": context,
                "reference_average_usd_per_million_tokens": None,
                "reason": "coût moyen non vérifiable : aucun tarif correspondant; seuil maximal de 0.5 $/M" if general_catalog else "coût moyen hors pointe non vérifiable : aucun tarif correspondant; seuil maximal de 0.5 $/M",
            })
            continue
        key = pricing_name(reference["name"])
        if key in matched_names and matched_names[key] != model_id:
            raise RuntimeError("plusieurs identifiants Go pour le même tarif : " + reference["name"])
        matched_names[key] = model_id
        average = prices["average"] if general_catalog else prices["average_off_peak"]
        if average > MAX_REFERENCE_AVERAGE_USD_PER_MILLION:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "context_length": context,
                "reference_average_usd_per_million_tokens": average,
                "pricing_variants": reference["variants"],
                "reason": f"coût moyen {average:g} $/M supérieur au seuil maximal de 0.5 $/M",
            })
            continue
        transport = go_transport(model, metadata, payload.get("retrieved_at"))
        row = {
            "id": model_id,
            "name": model.get("name") or model_id,
            "available": True,
            "api_metadata": {key: model.get(key) for key in ("object", "owned_by", "created") if key in model},
            **transport,
            "context_length": context,
            "context_status": "verified",
            "context_source": context_source,
            "pricing_status": "published",
            "pricing_source": pricing["source"],
            "pricing_retrieved_at": pricing["retrieved_at"],
            "pricing_variants": reference["variants"],
            **modality_info,
            "multimedia_status": "text_output" if modalities == ["text"] else "verified_output" if modalities else "not_verified",
            "reference_pricing_usd_per_million_tokens": prices,
            "quota_estimates_requests": {"rolling": None, "weekly": None, "monthly": None},
            "quota_estimates_status": "non collectées; N/A",
            "reference_average_usd_per_million_tokens": average,
        }
        known.append(row)
    known.sort(key=lambda row: (row["reference_average_usd_per_million_tokens"], row["id"]))
    for rank, row in enumerate(known, 1):
        row["rank"] = rank
    return known, excluded


def format_opencode_table(rows: list[dict], policy: str | None, generated_at: str, *, general_catalog: bool = False) -> str:
    lines = [
        "## Rapport des LMM du catalogue général OpenCode les moins onéreux" if general_catalog else "## Rapport des LMM OpenCode Go les moins onéreux",
        "",
        "Code couleur : 🟢 ≤ 0.20 $/M · 🟡 > 0.20 à 0.40 $/M · 🟠 > 0.40 à 0.50 $/M.",
        "",
        "| Rang | Modèle / ID | Contexte | Sortie | Entrée $/M | Sortie $/M | Coût moyen $/M | Code couleur |",
        "|---:|---|---:|---|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        prices = row["reference_pricing_usd_per_million_tokens"] or {}
        input_key, output_key, average_key = ("input", "output", "average") if general_catalog else ("input_off_peak", "output_off_peak", "average_off_peak")
        lines.append("| " + " | ".join(escape(value) for value in (
            row["rank"] if row["rank"] is not None else "—",
            f"{row['name']} ({row['id']})",
            context_label(row["context_length"]),
            "Texte" if row["output_modalities"] == ["text"] else ", ".join(row["output_modalities"]) if row["output_modalities"] else "Non vérifié",
            money(prices.get(input_key)),
            money(prices.get(output_key)),
            money(prices.get(average_key)),
            cost_color(prices.get(average_key)),
        )) + " |")
    lines.append("")
    if general_catalog:
        lines.append(f"Actualisé le {generated_at}; catalogue général OpenCode public, contexte ≥ 1M et coût moyen publié ≤ 0.5 $/M. Classement par coût moyen croissant.")
        lines.append("Les tarifs du catalogue général sont collectés indépendamment de Go. Le coût moyen maximal des variantes publiées est retenu ; les sources, dates et exclusions restent dans le JSON.")
    else:
        lines.append(f"Actualisé le {generated_at} avec la clé {policy}; classement par coût moyen hors pointe croissant, après filtres contexte ≥ 1M et coût moyen ≤ 0.5 $/M.")
        lines.append("Les tarifs sont des références OpenCode Go et peuvent évoluer. Les modèles exclus ne sont pas affichés dans les tableaux fournisseurs; leurs motifs restent disponibles dans le catalogue JSON.")
        lines.append("Tarifs collectés dans la documentation officielle; les variantes et la provenance restent dans le JSON. Pour plusieurs paliers de contexte, le coût moyen hors pointe maximal est retenu. Estimations de requêtes non collectées : N/A.")
    lines.append("Modalités et routage collectés sans liste de modèles; les sources et dates restent dans le JSON. Les routes documentées ne constituent pas un test de génération.")
    unrouted = [row["id"] for row in rows if row.get("routing_warning")]
    if unrouted:
        lines.append("Routes de génération non vérifiées : " + ", ".join(unrouted) + ".")
    return "\n".join(lines) + "\n"



OPENROUTER_API_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_SOURCE_URL = "https://openrouter.ai/models"
OPENROUTER_BLACKLIST = {"meta/muse-spark-1.2-contributor"}


def openrouter_number(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) and number >= 0 else None


def openrouter_money(value: float | None) -> str:
    if value is None:
        return "—"
    if value == 0:
        return "$0"
    return f"${value:.4f}".rstrip("0").rstrip(".")


def fetch_openrouter_models(api_key: str | None, timeout: float) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "TFL/1.0"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    with urlopen(Request(OPENROUTER_API_URL, headers=headers), timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise RuntimeError("réponse OpenRouter /models invalide")
    payload["pricing_source"] = OPENROUTER_API_URL
    payload["pricing_retrieved_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return payload


def openrouter_pricing_details(pricing: dict) -> dict:
    """Conserver les prix par million et les paliers sans modifier le classement API de base."""
    fields = ("prompt", "completion", "input_cache_read", "input_cache_write")
    unverified = []

    def converted(values: dict, prefix: str) -> dict:
        result = {}
        for field in fields:
            value = openrouter_number(values.get(field))
            amount = value * 1_000_000 if value is not None else None
            result[field] = amount if amount is not None and math.isfinite(amount) else None
            if field in values and result[field] is None:
                unverified.append(prefix + field)
        return result

    details = {"unit": "per_million_tokens", "currency": "USD",
               "selection_rule": "api_base_prompt_completion", "base": converted(pricing, "")}
    overrides = pricing.get("overrides", [])
    if not isinstance(overrides, list):
        raise RuntimeError("paliers tarifaires OpenRouter invalides")
    details["overrides"] = []
    for index, override in enumerate(overrides):
        if not isinstance(override, dict):
            raise RuntimeError("palier tarifaire OpenRouter invalide")
        conditions = {}
        if "min_prompt_tokens" in override:
            threshold = override["min_prompt_tokens"]
            if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 0:
                raise RuntimeError("seuil de palier tarifaire OpenRouter invalide")
            conditions["min_prompt_tokens"] = threshold
        if "utc_days" in override:
            days = override["utc_days"]
            weekdays = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
            if not isinstance(days, list) or not days or any(
                not isinstance(day, str) or day not in weekdays for day in days
            ):
                raise RuntimeError("jours UTC de palier tarifaire OpenRouter invalides")
            conditions["utc_days"] = days
        time_keys = ("utc_start", "utc_end")
        if any(key in override for key in time_keys):
            if not all(key in override for key in time_keys):
                raise RuntimeError("horaires UTC de palier tarifaire OpenRouter incomplets")
            for key in time_keys:
                value = override[key]
                if (isinstance(value, bool) or not isinstance(value, int)
                        or not 0 <= value <= 2359 or value % 100 >= 60):
                    raise RuntimeError("horaire UTC de palier tarifaire OpenRouter invalide")
                conditions[key] = value
        if not conditions:
            raise RuntimeError("condition de palier tarifaire OpenRouter non reconnue")
        details["overrides"].append({
            **conditions, **converted(override, f"overrides[{index}]."),
        })
    details["unverified_fields"] = unverified
    return details


def openrouter_output_label(modalities: list[str]) -> str:
    if modalities == ["text"]:
        return "Texte"
    return ", ".join(modalities) if modalities else "Non vérifié"


def build_openrouter_rows(payload: dict, blacklisted_models: tuple[str, ...] | None = None) -> tuple[list[dict], list[dict]]:
    blacklisted_models = blacklist.load_models() if blacklisted_models is None else blacklisted_models
    rows = []
    excluded = []
    for model in payload["data"]:
        if not isinstance(model, dict) or not model.get("id"):
            continue
        model_id = model["id"]
        if blacklist.is_blocked(model_id, blacklisted_models):
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "reason": "blacklist permanente" if model_id in OPENROUTER_BLACKLIST else "liste noire LM"})
            continue
        pricing = model.get("pricing") or {}
        architecture = model.get("architecture") or {}
        if not isinstance(pricing, dict) or not isinstance(architecture, dict):
            raise RuntimeError("métadonnées tarifaires OpenRouter invalides")
        input_modalities = sorted(str(value).lower() for value in architecture.get("input_modalities") or [])
        output_modalities = sorted(str(value).lower() for value in architecture.get("output_modalities") or [])
        context = positive_integer(model.get("context_length")) or 0
        if context < MIN_CONTEXT_TOKENS:
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "context_length": context, "reason": "contexte inférieur au seuil obligatoire de 1M"})
            continue
        non_text = sorted(set(output_modalities) & NON_TEXT_OUTPUT_MODALITIES)
        if non_text:
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "output_modalities": output_modalities, "reason": "sortie audio/vidéo exclue"})
            continue
        input_price = openrouter_number(pricing.get("prompt"))
        output_price = openrouter_number(pricing.get("completion"))
        if input_price is None or output_price is None:
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "reason": "coût moyen non vérifiable"})
            continue
        input_price *= 1_000_000
        output_price *= 1_000_000
        average = (input_price + output_price) / 2
        if not all(math.isfinite(value) for value in (input_price, output_price, average)):
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "reason": "coût moyen non vérifiable : débordement numérique"})
            continue
        if average > MAX_REFERENCE_AVERAGE_USD_PER_MILLION:
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "context_length": context, "reference_average_usd_per_million_tokens": average, "reason": "coût moyen supérieur au seuil maximal de 0.5 $/M"})
            continue
        supported = set(model.get("supported_parameters") or [])
        capabilities = []
        if "tools" in supported:
            capabilities.append("tools")
        if "reasoning" in supported or "include_reasoning" in supported:
            capabilities.append("reasoning")
        if "structured_outputs" in supported or "response_format" in supported:
            capabilities.append("JSON")
        rows.append({
            "rank": None,
            "id": model_id,
            "name": model.get("name") or model_id,
            "context_length": context,
            "output_label": openrouter_output_label(output_modalities),
            "input_price": input_price,
            "output_price": output_price,
            "average": average,
            "pricing_source": payload.get("pricing_source", OPENROUTER_API_URL),
            "pricing_retrieved_at": payload.get("pricing_retrieved_at"),
            "pricing_details": openrouter_pricing_details(pricing),
            "input_modalities": input_modalities,
            "output_modalities": output_modalities,
            "capabilities": capabilities,
            "api_metadata": {key: model.get(key) for key in ("object", "created", "owned_by") if key in model},
        })
    rows.sort(key=lambda row: (row["average"], row["input_price"], row["output_price"], row["id"]))
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    if not rows:
        raise RuntimeError("aucun modèle OpenRouter ne satisfait les filtres TFL")
    return rows, excluded


def format_openrouter_table(rows: list[dict], generated_at: str) -> str:
    lines = [
        "## Rapports des LMM OpenRouter les moins onéreux",
        "",
        "Code couleur : 🟢 ≤ 0.20 $/M · 🟡 > 0.20 à 0.40 $/M · 🟠 > 0.40 à 0.50 $/M.",
        "",
        "| Rang | Modèle / ID | Contexte | Sortie | Entrée $/M | Sortie $/M | Coût moyen $/M | Code couleur |",
        "|---:|---|---:|---|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape(value) for value in (
            row["rank"],
            f"{row['name']} ({row['id']})",
            context_label(row["context_length"]),
            row["output_label"],
            openrouter_money(row["input_price"]),
            openrouter_money(row["output_price"]),
            openrouter_money(row["average"]),
            cost_color(row["average"]),
        )) + " |")
    lines.append("")
    lines.append(f"Actualisé le {generated_at}; classement par coût moyen entrée/sortie croissant, après filtres contexte ≥ 1M et coût moyen ≤ 0.5 $/M.")
    lines.append("Les modèles multimodaux en entrée sont conservés; les métadonnées et capacités OpenRouter restent disponibles dans le catalogue JSON TFL.")
    lines.append("Sélection dynamique sur tout le catalogue API, sans liste prédéfinie; les modèles gratuits vérifiés sont admissibles et les exclusions restent auditables dans le JSON.")
    return "\n".join(lines) + "\n"


def openrouter_secret() -> str:
    result = subprocess.run(['secret-tool', 'lookup', 'service', 'pllm', 'policy', 'mode3',
                             'provider', 'openrouter', 'account', 'az.openrouter@pixs.fr'],
                            capture_output=True, timeout=15, check=False)
    if result.returncode or not result.stdout.strip():
        return ''
    return result.stdout.decode().strip()


def evaluate_free(model: dict, key: str, metadata: dict) -> dict:
    blacklist.require_allowed(model["model_id"])
    model.update(state='Invalide', cause='', reasoning='high', requested_reasoning='high',
                 evaluated_at=performance.now(), ttft_seconds=None, tokens_per_second=None,
                 performance_criteria=dict(performance.FREE_CRITERIA), quota_status='not_applicable',
                 throughput_metric=performance.THROUGHPUT_METRIC, throughput_window=performance.THROUGHPUT_WINDOW,
                 measurement_protocol_version=performance.MEASUREMENT_PROTOCOL_VERSION,
                 performance_test={'status': 'not_run', 'requests': 0})
    attempts = []
    previous_handler = signal.signal(signal.SIGALRM, performance.expire)
    try:
        if positive_integer(model.get('context_length')) is None or model['context_length'] < MIN_CONTEXT_TOKENS:
            raise RuntimeError('Contexte gratuit inférieur à 1M ou non vérifiable')
        if not key:
            raise RuntimeError('Clé API de génération inaccessible')
        protocol = model.get('api_protocol')
        endpoint = model.get('api_endpoint')
        if protocol not in ('responses', 'chat_completions', 'messages') or not isinstance(endpoint, str):
            raise RuntimeError('Routage absent ou protocole non benchmarké')
        if model['provider'] != 'openrouter':
            safe_go_url(endpoint)
        performance.reasoning(model, performance.BUDGETS[0], metadata)
        session_id = str(uuid.uuid4()) if model['provider'] != 'openrouter' else None
        pending = list(performance.BUDGETS)
        while pending:
            budget = pending.pop(0)
            try:
                try:
                    complete = performance.benchmark(model, key, budget, metadata, session_id=session_id)
                except (HTTPError, performance.ApiFailure) as error:
                    diagnostic = performance.http_diagnostic(error)
                    if not performance.can_retry_xhigh(model, metadata, diagnostic):
                        raise
                    attempts.append({**copy.deepcopy(model['performance_test']), 'status': 'failed',
                                     'max_tokens': budget, 'reasoning': 'high', 'http_error': copy.deepcopy(diagnostic)})
                    model['reasoning'] = 'xhigh'
                    pending = list(performance.BUDGETS)
                    budget = pending.pop(0)
                    complete = performance.benchmark(model, key, budget, metadata, session_id=session_id)
                if not complete:
                    raise RuntimeError('Budget du test épuisé : mesure inconclusive')
                try:
                    ttft, throughput = performance.finite(model['ttft_seconds']), performance.finite(model['tokens_per_second'])
                except (TypeError, ValueError) as error:
                    raise RuntimeError('Mesure de performance absente ou non finie') from error
                if ttft < 0 or ttft >= 30 or throughput <= 20:
                    raise RuntimeError('Seuil gratuit non satisfait : TTFT <30 s et débit >20 tokens/s requis')
            except Exception as error:
                diagnostic = performance.http_diagnostic(error) if isinstance(error, (HTTPError, performance.ApiFailure)) else None
                model['performance_test'].update(status='failed', max_tokens=budget, reasoning=model['reasoning'],
                                                 reason=performance.error_message(error))
                if diagnostic is not None:
                    model['performance_test']['http_error'] = copy.deepcopy(diagnostic)
                attempts.append(copy.deepcopy(model['performance_test']))
                if diagnostic is not None or isinstance(error, performance.AuthenticationFailure) or not pending:
                    raise
                continue
            model.update(state='Valide', cause='Tous les critères gratuits satisfaits')
            model['performance_test'].update(max_tokens=budget, reasoning=model['reasoning'])
            attempts.append(copy.deepcopy(model['performance_test']))
            break
    except Exception as error:
        model.update(state='Invalide', cause=performance.error_message(error))
        model['performance_test'].update(reason=model['cause'])
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)
        model['performance_test']['attempts'] = attempts
        for field in ('ttft_seconds', 'tokens_per_second'):
            if model.get(field) is not None:
                try:
                    model[field] = performance.finite(model[field])
                except (TypeError, ValueError):
                    model[field] = None
    return model


def qualify_free_models(rows: list[dict], excluded: list[dict], section: str,
                        key: str, audit: list[dict]) -> list[dict]:
    retained = []
    blacklisted_models = blacklist.load_models()
    for row in rows:
        if blacklist.is_blocked(row['id'], blacklisted_models):
            excluded.append({**row, 'reason': 'liste noire LM ou permanente'})
            continue
        row['is_free'] = performance.is_free(row, section)
        if not row['is_free']:
            retained.append(row)
            continue
        provider = {'opencode_go': 'opencodego', 'opencode': 'opencode', 'openrouter': 'openrouter'}[section]
        model = {'model_id': row['id'], 'provider': provider,
                 'api_protocol': row.get('api_protocol', 'chat_completions'),
                 'api_endpoint': row.get('api_endpoint') if section != 'openrouter' else 'https://openrouter.ai/api/v1/chat/completions',
                 'is_free': True, 'section': section, 'context_length': row.get('context_length')}
        evaluate_free(model, key, {'reasoning_capabilities': row.get('reasoning_capabilities', {})})
        audit.append(copy.deepcopy(model))
        row.update({field: copy.deepcopy(model[field]) for field in (
            'reasoning', 'requested_reasoning', 'evaluated_at', 'ttft_seconds', 'tokens_per_second',
            'performance_criteria', 'quota_status', 'performance_test',
            'throughput_metric', 'throughput_window', 'measurement_protocol_version')})
        if model['state'] == 'Valide':
            if isinstance(row.get('routing_metadata'), dict):
                row['routing_metadata']['generation_tested'] = True
            retained.append(row)
        else:
            excluded.append({**row, 'reason': model['cause'], 'performance_state': 'Invalide'})
    for rank, row in enumerate(retained, 1):
        row['rank'] = rank
    return retained


def format_free_performance(audit: list[dict]) -> str:
    lines = ['## Tests de performance des modèles gratuits', '',
             'Critères : contexte ≥1M, gratuité vérifiée, réponse complète, TTFT <30 s et débit >20 tokens/s. HIGH puis XHIGH si pris en charge ; aucun contrôle de quota.',
             'Débit moyen sur la requête complète, attente et TTFT inclus.', '',
             '| Fournisseur | Modèle / ID | TTFT (s) | Tokens/s | Raisonnement | État / cause |',
             '|---|---|---:|---:|---|---|']
    for model in audit:
        value = lambda field: '-' if model.get(field) is None else f'{model[field]:.4f}'
        state = ('🟢 Valide' if model['state'] == 'Valide' else '🔴 Exclu') + ' — ' + model['cause']
        lines.append('| ' + ' | '.join(escape(item) for item in (
            model['provider'], model['model_id'], value('ttft_seconds'), value('tokens_per_second'),
            model['reasoning'].upper(), state)) + ' |')
    if not audit:
        lines.append('Aucun candidat gratuit structurellement admissible.')
    return '\n'.join(lines) + '\n'


def main() -> int:
    args = parse_args()
    requested_policy = args.policy_option or args.policy or "auto"
    openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEY")
    api_key = ""
    try:
        blacklisted_models = blacklist.load_models()
        policy, api_key = select_secret(requested_policy)
        opencode_payload = fetch_models(api_key, args.timeout)
        go_metadata = fetch_go_metadata(args.timeout)
        go_pricing = fetch_go_pricing(args.timeout)
        opencode_rows, opencode_excluded = build_rows(opencode_payload, go_metadata, go_pricing, blacklisted_models=blacklisted_models)
        if not opencode_rows:
            raise RuntimeError("aucun modèle OpenCode Go ne satisfait les filtres TFL")
        general_payload = fetch_opencode_models(args.timeout)
        general_metadata = fetch_opencode_metadata(args.timeout)
        general_pricing = fetch_opencode_pricing(args.timeout)
        general_rows, general_excluded = build_rows(general_payload, general_metadata, general_pricing, general_catalog=True, blacklisted_models=blacklisted_models)
        if not general_rows:
            raise RuntimeError("aucun modèle du catalogue général OpenCode ne satisfait les filtres TFL")
        openrouter_payload = fetch_openrouter_models(openrouter_key, args.timeout)
        openrouter_rows, openrouter_excluded = build_openrouter_rows(openrouter_payload, blacklisted_models)
        audit = []
        for rows, payload, metadata in ((opencode_rows, opencode_payload, go_metadata),
                                        (general_rows, general_payload, general_metadata),
                                        (openrouter_rows, openrouter_payload, {})):
            raw_models = {row['id']: row for row in payload['data']}
            for row in rows:
                raw = raw_models.get(row['id'], {})
                row['reasoning_capabilities'] = performance.capabilities(raw, go_model_metadata(raw, metadata), row)
        if not openrouter_key and any(performance.is_free(row, 'openrouter') for row in openrouter_rows):
            try:
                openrouter_key = openrouter_secret()
            except (OSError, subprocess.SubprocessError):
                openrouter_key = ''
        opencode_rows = qualify_free_models(opencode_rows, opencode_excluded, 'opencode_go', api_key, audit)
        general_rows = qualify_free_models(general_rows, general_excluded, 'opencode', api_key, audit)
        openrouter_rows = qualify_free_models(openrouter_rows, openrouter_excluded, 'openrouter', openrouter_key or '', audit)
        if not all((opencode_rows, general_rows, openrouter_rows)):
            raise RuntimeError('aucun modèle admissible après qualification gratuite dans un catalogue ; rapports préservés')

    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"Erreur TFL: {exc}", file=sys.stderr)
        return 1
    finally:
        api_key = ""
        openrouter_key = ""

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    opencode_catalog = {
        "source_api": API_URL,
        "reference_source": SOURCE_URL,
        "pricing_reference": go_pricing,
        "context_metadata_source": CONTEXT_METADATA_URL,
        "model_metadata_source": go_metadata.get("source", CONTEXT_METADATA_URL),
        "model_metadata_retrieved_at": go_metadata.get("retrieved_at"),
        "credential_policy": policy,
        "source_model_count": len(opencode_payload["data"]),
        "excluded_model_count": len(opencode_excluded),
        "excluded_models": opencode_excluded,
        "models": opencode_rows,
    }
    openrouter_catalog = {
        "source_api": OPENROUTER_API_URL,
        "pricing_source": openrouter_payload.get("pricing_source", OPENROUTER_API_URL),
        "pricing_retrieved_at": openrouter_payload.get("pricing_retrieved_at"),
        "source_url": OPENROUTER_SOURCE_URL,
        "selection": "live-api-context-cost-modalities",
        "blacklist": {"model_ids": sorted(OPENROUTER_BLACKLIST), "policy": "permanent_exclusion"},
        "source_model_count": len(openrouter_payload["data"]),
        "excluded_model_count": len(openrouter_excluded),
        "excluded_models": openrouter_excluded,
        "models": openrouter_rows,
    }
    general_catalog = {
        "source_api": OPENCODE_API_URL,
        "reference_source": OPENCODE_SOURCE_URL,
        "pricing_reference": general_pricing,
        "metadata_provider": "opencode",
        "model_metadata_source": general_metadata.get("source", CONTEXT_METADATA_URL),
        "model_metadata_retrieved_at": general_metadata.get("retrieved_at"),
        "selection": "live-api-context-cost-modalities",
        "source_model_count": len(general_payload["data"]),
        "excluded_model_count": len(general_excluded),
        "excluded_models": general_excluded,
        "models": general_rows,
    }
    catalog = {
        "schema_version": 1,
        "measurement_protocol_version": performance.MEASUREMENT_PROTOCOL_VERSION,
        "throughput_metric": performance.THROUGHPUT_METRIC,
        "throughput_window": performance.THROUGHPUT_WINDOW,
        "free_performance_criteria": dict(performance.FREE_CRITERIA),
        "free_performance_results": audit,
        "generated_at": generated_at,
        "order": ["opencode_go", "opencode", "openrouter"],
        "common_columns": ["rank", "model_id", "context", "output", "input_price", "output_price", "average_cost", "cost_color"],
        "filters": {"minimum_context_tokens": MIN_CONTEXT_TOKENS, "maximum_average_usd_per_million_tokens": MAX_REFERENCE_AVERAGE_USD_PER_MILLION},
        "lm_blacklist": {"model_ids": list(blacklisted_models), "permanent_model_ids": list(blacklist.PERMANENT_MODELS)},
        "blacklists": {"opencode_go": sorted(BLACKLISTED_MODEL_IDS), "opencode": sorted(BLACKLISTED_MODEL_IDS), "openrouter": sorted(OPENROUTER_BLACKLIST)},
        "opencode_go": opencode_catalog,
        "opencode": general_catalog,
        "openrouter": openrouter_catalog,
    }
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "tfl.json"
    markdown_path = output_dir / "tfl.md"
    markdown = ("# TFL — Test Fournisseur LLM\n\n" + format_opencode_table(opencode_rows, policy, generated_at)
                + "\n" + format_opencode_table(general_rows, None, generated_at, general_catalog=True)
                + "\n" + format_openrouter_table(openrouter_rows, generated_at)
                + "\n" + format_free_performance(audit))
    try:
        serialized = json.dumps(catalog, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    except ValueError:
        print("Erreur TFL: catalogue non conforme au JSON strict", file=sys.stderr)
        return 1
    atomic_write(json_path, serialized)
    atomic_write(markdown_path, markdown)
    print(markdown, end="")
    print(f"Catalogue TFL JSON : {json_path}")
    print(f"Rapport TFL Markdown : {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
