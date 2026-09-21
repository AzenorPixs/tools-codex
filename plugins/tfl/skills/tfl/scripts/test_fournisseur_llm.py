#!/usr/bin/env python3
"""Générer le rapport unifié TFL des modèles OpenCode Go puis OpenRouter."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://opencode.ai/zen/go/v1/models"
SOURCE_URL = "https://opencode.ai/docs/go/"
CONTEXT_METADATA_URL = "https://models.dev/api.json"
ROOT = Path(__file__).resolve().parent.parent
MIN_CONTEXT_TOKENS = 1_000_000
MAX_REFERENCE_AVERAGE_USD_PER_MILLION = 0.5
BLACKLISTED_MODEL_IDS = {"muse-spark-1.2-contributor"}
NON_TEXT_OUTPUT_MODALITIES = {"audio", "video", "speech", "sound"}
KNOWN_TEXT_OUTPUT_IDS = {
    "grok-4.6", "gpt-5.6-luna", "glm-5.3-flash", "glm-5.3", "glm-5.2",
    "glm-5.1", "kimi-k3", "kimi-k2.7-code", "kimi-k2.6", "longcat-2.0",
    "deepseek-v4-pro", "deepseek-v4-flash", "deepseek-v4-flash-vision-exp",
    "mimo-v2-pro", "mimo-v2-omni", "mimo-v2.5-pro", "mimo-v2.5",
    "minimax-m3", "minimax-m2.7", "minimax-m2.5",
    "muse-spark-1.3-contributor",
    "qwen3.8-max", "qwen3.8-flash", "qwen3.7-max", "qwen3.7-plus",
    "qwen3.6-plus", "hy4-preview", "hy3", "omen-alpha",
}
POLICIES = {
    "mode1": "anthony.demard44@gmail.com",
    "mode2": "az.github@pixs.fr",
}

# Routage officiel OpenCode Go : le préfixe d’API n’est pas identique pour
# tous les modèles. Ces champs sont publiés afin que PLLM n’infère jamais une
# route à partir du seul nom du modèle.
OPENCODE_GO_ENDPOINTS = {
    "responses": "https://opencode.ai/zen/go/v1/responses",
    "messages": "https://opencode.ai/zen/go/v1/messages",
    "chat_completions": "https://opencode.ai/zen/go/v1/chat/completions",
}
OPENCODE_GO_RESPONSES_MODELS = {
    "muse-spark-1.3-contributor", "muse-spark-1.2-contributor",
    "gpt-5.6-luna", "grok-4.6",
}
OPENCODE_GO_MESSAGES_MODELS = {
    "minimax-m3", "minimax-m2.7", "minimax-m2.5",
    "qwen3.8-max", "qwen3.8-flash", "qwen3.7-max", "qwen3.7-plus",
    "qwen3.6-plus",
}


def opencode_go_api_route(model_id: str) -> tuple[str | None, str | None]:
    if model_id in OPENCODE_GO_RESPONSES_MODELS:
        protocol = "responses"
    elif model_id in OPENCODE_GO_MESSAGES_MODELS:
        protocol = "messages"
    elif model_id in KNOWN_TEXT_OUTPUT_IDS:
        protocol = "chat_completions"
    else:
        return None, None
    return OPENCODE_GO_ENDPOINTS[protocol], protocol

# Tarifs de référence publiés dans la documentation OpenCode Go. Les modèles
# absents de cette table restent visibles mais ne sont pas classés par défaut.
REFERENCE = {
    "grok-4.6": ({"input": 2.0, "output": 6.0}, {"rolling": 169, "weekly": 423, "monthly": 845}),
    "gpt-5.6-luna": ({"input": 0.2, "output": 1.2}, {"rolling": 2050, "weekly": 5100, "monthly": 10250}),
    "glm-5.3-flash": ({"input": 0.15, "output": 0.5}, {"rolling": 1580, "weekly": 3950, "monthly": 7900}),
    "glm-5.3": ({"input": 1.4, "output": 4.4}, {"rolling": 220, "weekly": 540, "monthly": 1080}),
    "glm-5.2": ({"input": 1.4, "output": 4.4}, {"rolling": 880, "weekly": 2150, "monthly": 4300}),
    "glm-5.1": ({"input": 1.4, "output": 4.4}, {"rolling": 880, "weekly": 2150, "monthly": 4300}),
    "kimi-k3": ({"input": 3.0, "output": 15.0}, {"rolling": 110, "weekly": 250, "monthly": 490}),
    "kimi-k2.7-code": ({"input": 0.95, "output": 4.0}, {"rolling": 1350, "weekly": 3380, "monthly": 6750}),
    "kimi-k2.6": ({"input": 0.95, "output": 4.0}, {"rolling": 1150, "weekly": 2880, "monthly": 5750}),
    "longcat-2.0": ({"input": 0.3, "output": 1.2}, {"rolling": 11400, "weekly": 28600, "monthly": 57200}),
    "deepseek-v4-pro": ({"input": 0.66, "output": 1.98, "peak_input": 1.32, "peak_output": 3.96}, {"rolling": 1050, "weekly": 2600, "monthly": 5200}),
    "deepseek-v4-flash": ({"input": 0.22, "output": 0.66, "peak_input": 0.44, "peak_output": 1.32}, {"rolling": 7600, "weekly": 18900, "monthly": 37800}),
    "deepseek-v4-flash-vision-exp": ({"input": 0.22, "output": 0.66, "peak_input": 0.44, "peak_output": 1.32}, {"rolling": 3800, "weekly": 9450, "monthly": 18900}),
    "mimo-v2.5": ({"input": 0.14, "output": 0.28}, {"rolling": 30100, "weekly": 75200, "monthly": 150400}),
    "mimo-v2.5-pro": ({"input": 0.435, "output": 0.87}, {"rolling": 3250, "weekly": 8150, "monthly": 16300}),
    "minimax-m3": ({"input": 0.3, "output": 1.2}, {"rolling": 3200, "weekly": 8000, "monthly": 16000}),
    "minimax-m2.7": ({"input": 0.3, "output": 1.2}, {"rolling": 3400, "weekly": 8500, "monthly": 17000}),
    "minimax-m2.5": ({"input": 0.3, "output": 1.2}, {"rolling": None, "weekly": None, "monthly": None}),
    "muse-spark-1.3-contributor": ({"input": 0.1, "output": 0.2}, {"rolling": 45300, "weekly": 113300, "monthly": 226600}),
    "qwen3.8-max": ({"input": 2.0, "output": 6.0}, {"rolling": 160, "weekly": 400, "monthly": 810}),
    "qwen3.8-flash": ({"input": 0.15, "output": 0.47}, {"rolling": 5400, "weekly": 13500, "monthly": 27000}),
    "qwen3.7-max": ({"input": 2.5, "output": 7.5}, {"rolling": 170, "weekly": 420, "monthly": 840}),
    "qwen3.7-plus": ({"input": 0.4, "output": 1.6}, {"rolling": 4300, "weekly": 10800, "monthly": 21600}),
    "qwen3.6-plus": ({"input": 0.5, "output": 3.0}, {"rolling": 3300, "weekly": 8200, "monthly": 16300}),
    "hy4-preview": ({"input": 0.834, "output": 2.501}, {"rolling": 1350, "weekly": 3380, "monthly": 6770}),
    "hy3": ({"input": 0.14, "output": 0.58}, {"rolling": 4300, "weekly": 10750, "monthly": 21500}),
    "omen-alpha": ({"input": 0.2, "output": 0.66}, {"rolling": 11600, "weekly": 29000, "monthly": 57900}),
}


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
    return payload


def fetch_context_metadata(timeout: float) -> dict:
    '''Récupérer les limites de contexte du fournisseur OpenCode Go.'''
    headers = {
        "Accept": "application/json",
        "User-Agent": "TOCG/1.0",
    }
    with urlopen(Request(CONTEXT_METADATA_URL, headers=headers), timeout=timeout) as response:
        payload = json.load(response)
    provider = payload.get("opencode-go") if isinstance(payload, dict) else None
    models = provider.get("models") if isinstance(provider, dict) else None
    if not isinstance(models, dict):
        raise RuntimeError("métadonnées de contexte OpenCode Go invalides")
    return models


def output_modalities(model: dict) -> list[str] | None:
    for key in ("output_modalities", "outputModalities"):
        values = model.get(key)
        if isinstance(values, list):
            return sorted(str(value).lower() for value in values)
    architecture = model.get("architecture")
    if isinstance(architecture, dict):
        values = architecture.get("output_modalities")
        if isinstance(values, list):
            return sorted(str(value).lower() for value in values)
    if model.get("id") in KNOWN_TEXT_OUTPUT_IDS:
        return ["text"]
    return None


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
    reference = metadata.get(model.get("id"))
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


def build_rows(payload: dict, metadata: dict) -> tuple[list[dict], list[dict]]:
    known = []
    unknown = []
    excluded = []
    for model in payload["data"]:
        if not isinstance(model, dict) or not model.get("id"):
            continue
        model_id = model["id"]
        if model_id in BLACKLISTED_MODEL_IDS:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "reason": "blacklist permanente",
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
        modalities = output_modalities(model)
        non_text = sorted(set(modalities or []) & NON_TEXT_OUTPUT_MODALITIES)
        if non_text:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "output_modalities": modalities,
                "reason": "sortie audio/vidéo exclue",
            })
            continue
        reference = REFERENCE.get(model_id)
        if reference is None:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "context_length": context,
                "reference_average_usd_per_million_tokens": None,
                "reason": "coût moyen non vérifiable; seuil maximal de 0.5 $/M",
            })
            continue
        prices, _estimates = reference
        average = (prices["input"] + prices["output"]) / 2
        if average > MAX_REFERENCE_AVERAGE_USD_PER_MILLION:
            excluded.append({
                "id": model_id,
                "name": model.get("name") or model_id,
                "context_length": context,
                "reference_average_usd_per_million_tokens": average,
                "reason": f"coût moyen {average:g} $/M supérieur au seuil maximal de 0.5 $/M",
            })
            continue
        row = {
            "id": model_id,
            "name": model.get("name") or model_id,
            "available": True,
            "api_metadata": {key: model.get(key) for key in ("object", "owned_by", "created") if key in model},
            "api_endpoint": opencode_go_api_route(model_id)[0],
            "api_protocol": opencode_go_api_route(model_id)[1],
            "endpoint_source": "opencode-go-docs",
            "context_length": context,
            "context_status": "verified",
            "context_source": context_source,
            "pricing_status": "published" if reference else "not_published",
            "output_modalities": modalities,
            "multimedia_status": "text_output" if modalities == ["text"] else "not_verified",
            "reference_pricing_usd_per_million_tokens": None,
            "quota_estimates_requests": None,
            "reference_average_usd_per_million_tokens": None,
        }
        if reference:
            prices, estimates = reference
            average = (prices["input"] + prices["output"]) / 2
            row["reference_pricing_usd_per_million_tokens"] = {
                "input_off_peak": prices["input"],
                "output_off_peak": prices["output"],
                "average_off_peak": average,
            }
            if "peak_input" in prices:
                row["reference_pricing_usd_per_million_tokens"].update({
                    "input_peak": prices["peak_input"],
                    "output_peak": prices["peak_output"],
                    "average_peak": (prices["peak_input"] + prices["peak_output"]) / 2,
                })
            row["quota_estimates_requests"] = estimates
            row["reference_average_usd_per_million_tokens"] = average
            known.append(row)
        else:
            unknown.append(row)
    known.sort(key=lambda row: (row["reference_average_usd_per_million_tokens"], row["id"]))
    for rank, row in enumerate(known, 1):
        row["rank"] = rank
    unknown.sort(key=lambda row: row["id"])
    for row in unknown:
        row["rank"] = None
    return known + unknown, excluded


def format_opencode_table(rows: list[dict], policy: str, generated_at: str) -> str:
    lines = [
        "## Rapport des LMM OpenCode Go les moins onéreux",
        "",
        "Code couleur : 🟢 ≤ 0.20 $/M · 🟡 > 0.20 à 0.40 $/M · 🟠 > 0.40 à 0.50 $/M.",
        "",
        "| Rang | Modèle / ID | Contexte | Sortie | Entrée $/M | Sortie $/M | Coût moyen $/M | Code couleur |",
        "|---:|---|---:|---|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        prices = row["reference_pricing_usd_per_million_tokens"] or {}
        lines.append("| " + " | ".join(escape(value) for value in (
            row["rank"] if row["rank"] is not None else "—",
            f"{row['name']} ({row['id']})",
            context_label(row["context_length"]),
            "Texte" if row["multimedia_status"] == "text_output" else "Non vérifié",
            money(prices.get("input_off_peak")),
            money(prices.get("output_off_peak")),
            money(prices.get("average_off_peak")),
            cost_color(prices.get("average_off_peak")),
        )) + " |")
    lines.append("")
    lines.append(f"Actualisé le {generated_at} avec la clé {policy}; classement par coût moyen hors pointe croissant, après filtres contexte ≥ 1M et coût moyen ≤ 0.5 $/M.")
    lines.append("Les tarifs et estimations sont des références OpenCode Go et peuvent évoluer. Les modèles exclus ne sont pas affichés dans le rapport Markdown; leurs motifs restent disponibles dans le catalogue JSON.")
    return "\n".join(lines) + "\n"



OPENROUTER_API_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_SOURCE_URL = "https://openrouter.ai/models?context=1000000&order=pricing-low-to-high&max_output_price=0.2&max_price=0.2&min_price=0.001&categories=programming"
OPENROUTER_BLACKLIST = {"meta/muse-spark-1.2-contributor"}
OPENROUTER_FIXED_IDS = (
    "qwen/qwen3.7-flash",
    "deepseek/deepseek-v4-flash-0731",
    "deepseek/deepseek-v4-flash",
)


def openrouter_number(value: object) -> float | None:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def openrouter_money(value: float | None) -> str:
    if value is None:
        return "—"
    if value == 0:
        return "$0"
    return f"${value:.4f}".rstrip("0").rstrip(".")


def fetch_openrouter_models(api_key: str | None, timeout: float) -> dict:
    query = {
        "sort": "pricing-low-to-high",
        "output_modalities": "text",
        "limit": "1000",
    }
    url = f"{OPENROUTER_API_URL}?{urlencode(query)}"
    headers = {"Accept": "application/json", "User-Agent": "TFL/1.0"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    with urlopen(Request(url, headers=headers), timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise RuntimeError("réponse OpenRouter /models invalide")
    return payload


def openrouter_output_label(modalities: list[str]) -> str:
    if modalities == ["text"]:
        return "Texte"
    return ", ".join(modalities) if modalities else "Non vérifié"


def build_openrouter_rows(payload: dict) -> tuple[list[dict], list[dict]]:
    rows = []
    excluded = []
    seen = set()
    for model in payload["data"]:
        if not isinstance(model, dict) or not model.get("id"):
            continue
        model_id = model["id"]
        if model_id not in OPENROUTER_FIXED_IDS:
            continue
        seen.add(model_id)
        if model_id in OPENROUTER_BLACKLIST:
            excluded.append({"id": model_id, "name": model.get("name") or model_id, "reason": "blacklist permanente"})
            continue
        pricing = model.get("pricing") or {}
        architecture = model.get("architecture") or {}
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
            "input_modalities": input_modalities,
            "output_modalities": output_modalities,
            "capabilities": capabilities,
            "api_metadata": {key: model.get(key) for key in ("object", "created", "owned_by") if key in model},
        })
    missing = [model_id for model_id in OPENROUTER_FIXED_IDS if model_id not in seen]
    if missing:
        raise RuntimeError("modèle(s) OpenRouter figé(s) absent(s) de l’API: " + ", ".join(missing))
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
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    requested_policy = args.policy_option or args.policy or "auto"
    openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEY")
    api_key = ""
    try:
        policy, api_key = select_secret(requested_policy)
        opencode_payload = fetch_models(api_key, args.timeout)
        context_metadata = fetch_context_metadata(args.timeout)
        opencode_rows, opencode_excluded = build_rows(opencode_payload, context_metadata)
        if not opencode_rows:
            raise RuntimeError("aucun modèle OpenCode Go ne satisfait les filtres TFL")
        openrouter_payload = fetch_openrouter_models(openrouter_key, args.timeout)
        openrouter_rows, openrouter_excluded = build_openrouter_rows(openrouter_payload)
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
        "context_metadata_source": CONTEXT_METADATA_URL,
        "credential_policy": policy,
        "source_model_count": len(opencode_payload["data"]),
        "excluded_model_count": len(opencode_excluded),
        "excluded_models": opencode_excluded,
        "models": opencode_rows,
    }
    openrouter_catalog = {
        "source_api": OPENROUTER_API_URL,
        "source_url": OPENROUTER_SOURCE_URL,
        "selection": "fixed-web-programming-low-cost",
        "blacklist": {"model_ids": sorted(OPENROUTER_BLACKLIST), "policy": "permanent_exclusion"},
        "source_model_count": len(openrouter_payload["data"]),
        "excluded_model_count": len(openrouter_excluded),
        "excluded_models": openrouter_excluded,
        "models": openrouter_rows,
    }
    catalog = {
        "schema_version": 1,
        "generated_at": generated_at,
        "order": ["opencode_go", "openrouter"],
        "common_columns": ["rank", "model_id", "context", "output", "input_price", "output_price", "average_cost", "cost_color"],
        "filters": {"minimum_context_tokens": MIN_CONTEXT_TOKENS, "maximum_average_usd_per_million_tokens": MAX_REFERENCE_AVERAGE_USD_PER_MILLION},
        "blacklists": {"opencode_go": sorted(BLACKLISTED_MODEL_IDS), "openrouter": sorted(OPENROUTER_BLACKLIST)},
        "opencode_go": opencode_catalog,
        "openrouter": openrouter_catalog,
    }
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "tfl.json"
    markdown_path = output_dir / "tfl.md"
    markdown = "# TFL — Test Fournisseur LLM\n\n" + format_opencode_table(opencode_rows, policy, generated_at) + "\n" + format_openrouter_table(openrouter_rows, generated_at)
    atomic_write(json_path, json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    atomic_write(markdown_path, markdown)
    print(markdown, end="")
    print(f"Catalogue TFL JSON : {json_path}")
    print(f"Rapport TFL Markdown : {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
