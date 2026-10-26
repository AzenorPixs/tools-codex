#!/usr/bin/env python3
"""Evaluate PLLM quotas before bounded streaming benchmarks; publish no secrets."""
import json
import importlib.util
import argparse
import copy
import math
import re
import signal
import subprocess
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from email.utils import parsedate_to_datetime
from http.client import HTTPException
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
PROMPT = 'Write only Python code for a stable merge_sort(values) function and three assert tests. No explanation.'
BUDGETS = (1024, 2048, 4096, 8192)
TTFT_LIMIT_SECONDS = 90
FREE_MODES = ('mode3', 'mode4')
POLICY_PROVIDERS = ('opencodego', 'opencodego', 'opencodego', 'opencodego', 'openrouter', 'deepseek')
SECRET_POLICIES = ('mode1', 'mode2', 'mode1', 'mode2', 'mode3', 'mode4')
SECRET_ACCOUNT_INDICES = (0, 1, 0, 1, 2, 3)
MEMORY_PATH = ROOT / 'data/pllm-performance-memory.json'
_PERFORMANCE_SPEC = importlib.util.spec_from_file_location('pllm_performance', Path(__file__).with_name('performance.py'))
performance = importlib.util.module_from_spec(_PERFORMANCE_SPEC)
_PERFORMANCE_SPEC.loader.exec_module(performance)


OPENCODE_GO_ROUTE_BY_MODEL = {
    'muse-spark-1.3-contributor': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
    'muse-spark-1.2-contributor': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
    'gpt-5.6-luna': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
    'grok-4.6': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
}

ACCOUNTS = ['anthony.demard44@gmail.com', 'az.github@pixs.fr', 'az.openrouter@pixs.fr', 'az.deepseek@pixs.fr']


class QuotaExhausted(RuntimeError):
    """Resource exhaustion established from a complete authenticated response."""


class AuthenticationFailure(RuntimeError):
    """Authentication failed; do not hide it behind another candidate."""


class ResourceFailure(RuntimeError):
    """An indispensable resource control failed during candidate evaluation."""


class CategoryChanged(RuntimeError):
    def __init__(self, category):
        super().__init__('Ressources modifiées : nouvelle catégorie ' + category)
        self.category = category


class ApiFailure(RuntimeError):
    def __init__(self, diagnostic):
        super().__init__(http_error_text(diagnostic))
        self.diagnostic = diagnostic


def retry_after(value, reference=None):
    result = {'retry_after_seconds': None, 'retry_at': None}
    if not isinstance(value, str) or not value or len(value) > 128:
        return result
    value = value.strip()
    reference = reference or datetime.now(timezone.utc)
    try:
        if re.fullmatch(r'[0-9]+', value):
            delay = int(value)
            target = reference + timedelta(seconds=delay)
        else:
            target = parsedate_to_datetime(value)
            if target.tzinfo is None:
                return result
            delay = max(0, math.ceil((target - reference).total_seconds()))
            target = max(target, reference)
        target.astimezone(ZoneInfo('Europe/Paris'))
        result.update(retry_after_seconds=delay, retry_at=target.isoformat(timespec='seconds'))
    except (ValueError, TypeError, OverflowError):
        pass
    return result


def filtered_error(payload):
    codes, parameters, messages = [], [], []
    known_codes = {'invalid_request_error', 'invalid_value', 'unsupported_parameter', 'rate_limit_exceeded',
                   'rate_limit_error', 'too_many_requests', 'FreeUsageLimitError', 'free_usage_limit',
                   'MissingSessionID', 'invalid_api_key', 'authentication_error', 'permission_denied'}
    known_parameters = ('thinking', 'reasoning_effort', 'reasoning.effort', 'output_config.effort', 'max_tokens',
                        'max_output_tokens', 'stream_options', 'x-opencode-session', 'model')

    def collect(value, depth=0):
        if depth > 4:
            return
        if isinstance(value, dict):
            for field in ('code', 'type', 'name'):
                item = value.get(field)
                if isinstance(item, str) and item in known_codes:
                    codes.append(item)
            for field in ('param', 'parameter'):
                item = value.get(field)
                if isinstance(item, str) and item in known_parameters:
                    parameters.append(item)
            for field in ('error', 'message', 'detail', 'errors', 'data'):
                item = value.get(field)
                if isinstance(item, str):
                    messages.append(item)
                else:
                    collect(item, depth + 1)
        elif isinstance(value, list):
            for item in value[:32]:
                collect(item, depth + 1)

    collect(payload)
    text = ' '.join(messages).lower()
    unsupported = 'unsupported_parameter' in codes or bool(re.search(
        r'unsupported|not support|unrecognized|unknown parameter|not allowed', text))
    if unsupported and not parameters:
        parameters = [name for name in known_parameters
                      if re.search(r'(?<![\w.])' + re.escape(name) + r'(?![\w.])', text)]
    return {'error_code': codes[0] if codes else None,
            'parameter': parameters[0] if parameters else None,
            'unsupported_parameter': unsupported,
            'free_usage_limit': bool(re.search(r'free.{0,40}(usage|limit)|(usage|limit).{0,40}free', text)),
            'model_limit': bool(re.search(r'for (this|the) model|model.{0,30}limit|limit.{0,30}model', text))}


def http_diagnostic(error):
    if isinstance(error, ApiFailure):
        return error.diagnostic
    cached = getattr(error, 'pllm_diagnostic', None)
    if cached is not None:
        return cached
    diagnostic = {'http_status': error.code, 'body_status': 'unavailable'}
    diagnostic.update(retry_after(error.headers.get('Retry-After') if error.headers else None))
    payload = None
    try:
        raw = error.read(65536)
        diagnostic['body_status'] = 'too_large' if len(raw) == 65536 else 'json'
        if len(raw) < 65536:
            payload = json.loads(raw)
    except (OSError, ValueError, UnicodeError, RecursionError, HTTPException):
        diagnostic['body_status'] = 'unreadable_or_not_json'
    finally:
        error.close()
    diagnostic.update(filtered_error(payload))
    error.pllm_diagnostic = diagnostic
    return diagnostic


def http_error_text(diagnostic):
    status = diagnostic['http_status']
    if status in (401, 403):
        return 'Authentification refusée (HTTP 401)' if status == 401 else 'Accès refusé (HTTP 403)'
    if status == 400:
        if diagnostic.get('error_code') == 'MissingSessionID':
            return 'HTTP 400 — session OpenCode manquante'
        if diagnostic.get('parameter'):
            reason = 'paramètre non pris en charge' if diagnostic.get('unsupported_parameter') else 'paramètre invalide'
            return 'HTTP 400 — ' + reason + ' : ' + diagnostic['parameter']
    message = 'HTTP ' + str(status)
    if status == 429:
        message += ' — limite d’usage gratuit' if diagnostic.get('free_usage_limit') else ' — limitation fournisseur'
        if diagnostic.get('model_limit'):
            message += ' du modèle'
        if diagnostic.get('retry_at'):
            target = datetime.fromisoformat(diagnostic['retry_at']).astimezone(ZoneInfo('Europe/Paris'))
            message += ' ; réessai à partir du ' + target.strftime('%d-%m-%y %H:%M') + ' (Paris)'
    return message


def api_error(code, payload=None):
    if code in (401, '401', 'invalid_api_key', 'authentication_error', 'unauthorized'):
        return AuthenticationFailure('Authentification refusée (HTTP 401)')
    if code in (403, '403', 'permission_denied', 'forbidden'):
        return ApiFailure({'http_status': 403, **filtered_error(payload)})
    if code in (429, '429', 'rate_limit_exceeded', 'rate_limit_error', 'too_many_requests',
                'FreeUsageLimitError', 'free_usage_limit'):
        return ApiFailure({'http_status': 429, **filtered_error(payload)})
    if code in (400, '400', 'invalid_request_error', 'invalid_value', 'unsupported_parameter'):
        return ApiFailure({'http_status': 400, **filtered_error(payload)})
    return RuntimeError('Erreur dans le flux API')


def error_message(error):
    if isinstance(error, (urllib.error.HTTPError, ApiFailure)):
        return http_error_text(http_diagnostic(error))
    return str(error) if isinstance(error, RuntimeError) else type(error).__name__


def is_authentication_error(error):
    return isinstance(error, AuthenticationFailure) or (
        isinstance(error, urllib.error.HTTPError) and error.code == 401)


def now():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def expire(signum, frame):
    raise TimeoutError('Request deadline exceeded')


def finite(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError('Nonfinite measurement')
    return number


def request(url, key, body=None, extra_headers=None):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'PLLM-coding-agent/1.0'}
    if key and not (extra_headers and 'x-api-key' in extra_headers):
        headers['Authorization'] = 'Bearer ' + key
    if extra_headers:
        headers.update(extra_headers)
    return urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), headers=headers), timeout=45)


def get(url, key):
    signal.alarm(50)
    try:
        with request(url, key) as response:
            return json.load(response)
    finally:
        signal.alarm(0)


def quota(m, key):
    if m['mode'] in FREE_MODES:
        m.update(quotas=None, quota_status='not_applicable')
        return
    provider = 'opencodego' if m['mode'] in ('mode1', 'mode2') else m['provider']
    m['quota_provider'] = provider
    if provider == 'opencodego':
        q = get('https://opencode.ai/zen/go/v1/usage', key)['usage']
        m['quotas'] = q
        periods = ('rolling', 'weekly', 'monthly')
        values = {p: finite(q[p]['percent']) for p in periods}
        if any(values[p] < 0 or q[p]['status'] not in ('ok', 'rate-limited') for p in periods):
            raise RuntimeError('Données de quota indisponibles ou incohérentes')
        m['quotas_evaluated_at'] = now()
        failed = [p for p in periods if values[p] >= 100]
        if failed:
            raise QuotaExhausted('Quota épuisé : ' + ', '.join(failed))
        if any(q[p]['status'] != 'ok' for p in periods):
            raise RuntimeError('Quota indisponible sans épuisement confirmé')
    elif provider == 'openrouter':
        q = get('https://openrouter.ai/api/v1/credits', key)['data']
        balance = finite(q['total_credits']) - finite(q['total_usage'])
        m['quotas'] = {'balance': balance, 'currency': 'USD'}
        m['quotas_evaluated_at'] = now()
        if balance <= 0:
            raise QuotaExhausted('Crédit épuisé')
    else:
        q = get('https://api.deepseek.com/user/balance', key)
        m['quotas'] = q
        if q['is_available'] is not True or not any(finite(b['total_balance']) > 0 for b in q['balance_infos']):
            raise RuntimeError('Solde indisponible ou épuisé')
    m['quotas_evaluated_at'] = now()


def reasoning(m, budget, metadata):
    return performance.reasoning(m, budget, metadata)


def benchmark(m, key, budget, metadata, session_id=None):
    return performance.run_benchmark(m, key, budget, metadata, session_id,
                                     reasoning=reasoning, request=request, now=now, api_error=api_error,
                                     clock=time.monotonic, alarm=signal.alarm)


def availability_color(remaining_percent):
    if remaining_percent >= 75:
        return 'green', '🟢'
    if remaining_percent >= 50:
        return 'yellow', '🟡'
    if remaining_percent >= 25:
        return 'orange', '🟠'
    return 'red', '🔴'


def exchange_rates():
    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    with urllib.request.urlopen(url, timeout=15) as response:
        root = ET.fromstring(response.read())
    return {'source': url, 'date': next(e.attrib['time'] for e in root.iter() if 'time' in e.attrib),
            'rates': {e.attrib['currency']: finite(e.attrib['rate']) for e in root.iter() if 'currency' in e.attrib}}


def quota_display(m, fx=None):
    if m['mode'] in FREE_MODES:
        return {'text': 'Non applicable — mode gratuit sans contrôle de quota', 'items': []}
    q = m.get('quotas')
    if not q:
        return {'text': '⚪ Non disponible', 'items': []}
    items = []
    if m.get('quota_provider', m['provider']) == 'opencodego':
        for period, label in [('rolling', '5 h'), ('weekly', 'Semaine'), ('monthly', 'Mois')]:
            value = q.get(period, {}).get('percent')
            if value is None:
                continue
            remaining = max(0, min(100, 100 - finite(value)))
            color, symbol = availability_color(remaining)
            display_label = 'Hebdo' if period == 'weekly' else label
            items.append({'period': period, 'remaining_percent': remaining, 'color': color,
                          'text': f'{symbol} {display_label} : {remaining:g} %'})
    else:
        balances = [{'currency': q.get('currency'), 'total_balance': q.get('balance')}] if 'balance' in q else q.get('balance_infos', [])
        for balance in balances:
            currency = balance.get('currency')
            value = balance.get('total_balance')
            if value is None:
                continue
            value = finite(value)
            # A EUR threshold cannot be silently applied to USD or CNY.
            rate = 1 if currency == 'EUR' else (fx or {}).get('rates', {}).get(currency)
            if rate is None or rate <= 0:
                items.append({'currency': currency, 'balance': value, 'color': None,
                              'reference_eur': 20, 'text': f'⚪ {value:g} $ — couleur EUR non calculée (conversion requise)'})
                continue
            eur = value / rate
            color, symbol = availability_color(max(0, min(100, eur / 20 * 100)))
            items.append({'currency': currency, 'balance': value, 'balance_eur': eur, 'reference_eur': 20, 'color': color, 'exchange_rate_date': (fx or {}).get('date'),
                          'text': f'{symbol} {value:g} $'})
    return {'text': ' ; '.join(x['text'] for x in items) or 'Non disponible', 'items': items}


def performance_color(metric, value, mode=None):
    if value is None:
        return '⚪'
    if mode in FREE_MODES and ((metric == 'ttft' and value >= 30) or (metric != 'ttft' and value <= 20)):
        return '🔴'
    if metric == 'ttft':
        if value < 30:
            return '🟢'
        if value < 45:
            return '🟡'
        if value < TTFT_LIMIT_SECONDS:
            return '🟠'
        return '🔴'
    if value > 30:
        return '🟢'
    if value >= 20:
        return '🟡'
    if value > 15:
        return '🟠'
    return '🔴'


def performance_display(metric, value, scope=None, mode=None):
    if value is None:
        return '-'
    symbol = performance_color(metric, value, mode)
    if metric == 'ttft':
        return f'{symbol} {value:.1f} s'
    return f'{symbol} {value:.1f}'


def display_timestamp(value):
    if not value:
        return '-'
    try:
        return datetime.fromisoformat(str(value)).astimezone().strftime('%d-%m-%y %H:%M')
    except (TypeError, ValueError):
        return str(value)


def markdown_text(value):
    """Keep values inside a Markdown table cell without breaking its syntax."""
    return str(value).replace('\n', ' ').replace('|', '\\|')


def policy_table(models):
    """Render all evaluated policies in one native Markdown table."""
    headers = [
        'Politique', 'Identifiant API', 'Fournisseur', 'TTFT (s)', 'Tokens/s', 'État',
        'Dernier palier réussi', 'Évalué le',
    ]
    lines = [
        '| ' + ' | '.join(headers) + ' |',
        '|' + '|'.join('---' for _ in headers) + '|',
    ]
    for model in models:
        values = [
            model['mode'],
            model.get('model_id', model['model']),
            model['provider'],
            performance_display('ttft', model.get('ttft_seconds'), mode='mode3' if model.get('is_free') else model['mode']),
            performance_display('tokens', model.get('tokens_per_second'), model.get('throughput_scope'), 'mode3' if model.get('is_free') else model['mode']),
            ('🟢 Valide' + (' — gratuit' if model['mode'] in FREE_MODES else '')
             if model['state'] == 'Valide' else '🔴 Invalide — ' + (model.get('cause') or 'Non évalué')),
            model.get('last_successful_max_tokens') or '-',
            display_timestamp(model.get('evaluated_at')),
        ]
        lines.append('| ' + ' | '.join(markdown_text(value) for value in values) + ' |')
    return '\n'.join(['### Rapport PLLM', '',
                      'Débit moyen sur la requête complète, attente et TTFT inclus.', '', *lines])


def quota_summary(models):
    lines = ['Quotas / soldes :']
    lines.extend(
        f'{model["mode"]} : {model.get("quota_display", {}).get("text") or "⚪ Non disponible"}'
        for model in models
    )
    return '\n'.join(lines)


def active_summary(models):
    selected = next((model for model in models if model.get('selected')), None)
    if selected is None:
        return '### **PLLM active : aucune politique valide**'
    model_name = selected.get('model') or selected.get('model_id') or '-'
    return (f'### **PLLM active : {selected["mode"]} | '
            f'Fournisseur : {selected["provider"]} | Modèle : {model_name}**')


def publish(d, active=False, forced_mode=None):
    try:
        fx = exchange_rates()
    except Exception as error:
        fx = None
        d['quota_color_warning'] = 'Conversion EUR indisponible : ' + type(error).__name__
    else:
        d.pop('quota_color_warning', None)
    d['quota_exchange_rates'] = fx
    chosen = next((m for m in d['models'] if m['state'] == 'Valide' and m.get('evaluated_this_run', True)), None)
    for m in d['models']:
        m['selected'] = m is chosen
        m['quota_display'] = quota_display(m, fx)
    d.update(published_at=now(), evaluated_at=now(), selected_mode=chosen['mode'] if chosen else None,
             selection_status='selected' if chosen else 'no_valid_model', protocol_version=performance.MEASUREMENT_PROTOCOL_VERSION)
    d.pop('last_partial_evaluation_at', None)
    if forced_mode:
        models = [m for m in d['models'] if m.get('evaluated_this_run') and m['mode'] == forced_mode]
    else:
        models = [chosen] if active and chosen else ([] if active else d['models'])
    if models:
        content = policy_table(models) + '\n\n' + quota_summary(models) + '\n\n' + active_summary(d['models']) + '\n'
    else:
        content = '**Aucune politique valide**\n'
    (ROOT / 'data').mkdir(parents=True, exist_ok=True)
    for name, output in [('pllm-current.json', json.dumps(d, ensure_ascii=False, indent=2) + '\n'), ('pllm-current.md', content)]:
        p = ROOT / 'data' / name
        temp = p.with_name(p.name + '.tmp')
        temp.write_text(output, encoding='utf-8')
        temp.replace(p)
    if not active:
        print(content, flush=True)


def load_tfl_catalog(catalog_path=None):
    path = Path(catalog_path) if catalog_path is not None else ROOT.parent / 'tfl/data/tfl.json'
    try:
        catalog = json.loads(path.read_text(encoding='utf-8'), parse_float=finite, parse_constant=finite)
    except (OSError, ValueError) as error:
        raise RuntimeError('Catalogue TFL absent, illisible ou invalide') from error
    if not isinstance(catalog, dict):
        raise RuntimeError('Catalogue TFL invalide : objet attendu')
    return catalog


def tfl_opencode_model_at(rank, catalog_path=None):
    catalog = load_tfl_catalog(catalog_path)
    if not isinstance(catalog.get('opencode_go'), dict):
        raise RuntimeError('Section TFL OpenCode Go absente ou invalide')
    models = catalog.get('opencode_go', {}).get('models')
    if not isinstance(models, list) or not models:
        raise RuntimeError('Catalogue TFL OpenCode Go vide ou invalide')
    if not isinstance(rank, int) or rank < 1 or rank > len(models):
        raise RuntimeError(f'Rang OpenCode Go TFL indisponible : {rank}')
    model = models[rank - 1]
    if not isinstance(model, dict):
        raise RuntimeError('Modèle TFL OpenCode Go invalide')
    model_id = model.get('id')
    if not isinstance(model_id, str) or not model_id:
        raise RuntimeError('Identifiant du modèle OpenCode Go TFL absent')
    endpoint, protocol = model.get('api_endpoint'), model.get('api_protocol')
    if not endpoint or not protocol:
        endpoint, protocol = OPENCODE_GO_ROUTE_BY_MODEL.get(model_id, (None, None))
    if not endpoint or not protocol:
        raise RuntimeError('Routage API OpenCode Go absent ou non vérifié dans le catalogue TFL')
    if protocol not in ('responses', 'chat_completions', 'messages'):
        raise RuntimeError('Protocole API OpenCode Go non benchmarké par PLLM : ' + protocol)
    model = dict(model)
    model['api_endpoint'] = endpoint
    model['api_protocol'] = protocol
    return model, catalog.get('generated_at')


def cheapest_tfl_opencode_model():
    return tfl_opencode_model_at(1)


def next_tfl_opencode_model(current_id, catalog_path=None):
    catalog = load_tfl_catalog(catalog_path)
    if not isinstance(catalog.get('opencode_go'), dict):
        raise RuntimeError('Section TFL OpenCode Go absente ou invalide')
    models = catalog.get('opencode_go', {}).get('models')
    if not isinstance(models, list):
        return None
    found = False
    for candidate in models:
        if not isinstance(candidate, dict) or not isinstance(candidate.get('id'), str) or not candidate['id']:
            raise RuntimeError('Modèle TFL OpenCode Go invalide')
        if candidate.get('id') == current_id:
            found = True
            continue
        if not found or candidate.get('available') is not True:
            continue
        endpoint = candidate.get('api_endpoint')
        protocol = candidate.get('api_protocol')
        if protocol not in ('responses', 'chat_completions', 'messages') or not endpoint:
            continue
        result = dict(candidate)
        result['api_endpoint'] = endpoint
        result['api_protocol'] = protocol
        return result
    return None


def load_memory():
    if not MEMORY_PATH.exists():
        return {'schema_version': 2, 'policies': {}}
    try:
        memory = json.loads(MEMORY_PATH.read_text(encoding='utf-8'))
        if (not isinstance(memory, dict) or memory.get('schema_version') not in (1, 2)
                or not isinstance(memory.get('policies'), dict)
                or any(not isinstance(value, dict) for value in memory['policies'].values())):
            raise ValueError('Structure de mémoire invalide')
        allowed = {f'mode{i}' for i in range(1, 5 if memory['schema_version'] == 1 else 7)}
        if not set(memory['policies']).issubset(allowed):
            raise ValueError('Politiques de mémoire invalides')
    except (OSError, ValueError) as error:
        raise RuntimeError('Mémoire de performance PLLM invalide ; fichier préservé') from error
    if memory['schema_version'] == 1:
        memory['policies'] = {({'mode3': 'mode5', 'mode4': 'mode6'}.get(mode, mode)): value
                              for mode, value in memory['policies'].items()}
        memory.update(schema_version=2, migrated_from_schema_version=1)
    return memory


def identity(m):
    return {k: m.get(k) for k in ('model_id', 'provider', 'reasoning', 'throughput_scope', 'api_protocol', 'api_endpoint',
                                    'throughput_metric', 'throughput_window', 'measurement_protocol_version')}


def budgets_for(m, memory):
    previous = memory['policies'].get(m['mode'], {})
    previous = previous.get('configurations', {}).get(json.dumps(identity(m), sort_keys=True), previous)
    budget = previous.get('last_successful_max_tokens')
    if previous.get('identity') == identity(m) and budget in BUDGETS:
        m['last_successful_max_tokens'] = budget
        return BUDGETS[BUDGETS.index(budget):]
    m['last_successful_max_tokens'] = None
    return BUDGETS


def remember_success(m, budget, memory):
    previous = memory['policies'].get(m['mode'], {})
    configurations = dict(previous.get('configurations', {}))
    if 'identity' in previous:
        configurations[json.dumps(previous['identity'], sort_keys=True)] = {
            k: v for k, v in previous.items() if k != 'configurations'}
    success = {
        'identity': identity(m), 'last_successful_max_tokens': budget,
        'succeeded_at': now(), 'ttft_seconds': m['ttft_seconds'],
        'tokens_per_second': m['tokens_per_second'],
    }
    configurations[json.dumps(identity(m), sort_keys=True)] = dict(success)
    memory['policies'][m['mode']] = {**success, 'configurations': configurations}
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp = MEMORY_PATH.with_name(MEMORY_PATH.name + '.tmp')
    temp.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(MEMORY_PATH)
    m['last_successful_max_tokens'] = budget


def performance_limits(model):
    return performance.limits(model)


def initial_model(priority, provider):
    mode = f'mode{priority}'
    ttft, throughput = performance_limits({'mode': mode})
    return {'mode': mode, 'priority': priority, 'provider': provider,
            'model': 'Non évalué', 'reasoning': 'high', 'state': 'Invalide',
            'condition': f'TTFT < {ttft} s ET tokens/s > {throughput} ET ' + (
                'gratuité vérifiée ET contexte >= 1M' if mode in FREE_MODES else
                'candidat payant ET solde > 0' if mode == 'mode5' else
                'is_available=true ET au moins un solde utilisable > 0' if mode == 'mode6' else 'quotas valides'),
            'performance_criteria': {'ttft_lt_seconds': ttft, 'tokens_per_second_gt': throughput},
            'throughput_metric': performance.THROUGHPUT_METRIC, 'throughput_window': performance.THROUGHPUT_WINDOW,
            'measurement_protocol_version': performance.MEASUREMENT_PROTOCOL_VERSION,
            'quota_status': 'not_applicable' if mode in FREE_MODES else 'not_evaluated',
            'selected': False, 'evaluated_this_run': False, 'evaluated_at': None,
            'ttft_seconds': None, 'tokens_per_second': None, 'quotas': None,
            'cause': 'Non évalué', 'performance_test': {'status': 'not_run'}}


def load_current():
    try:
        data = json.loads((ROOT / 'data/pllm-current.json').read_text(encoding='utf-8'), parse_float=finite, parse_constant=finite)
    except FileNotFoundError:
        return {'schema_version': 2, 'selected_mode': None, 'selection_status': 'no_valid_model',
                'models': [initial_model(priority, provider)
                           for priority, provider in enumerate(POLICY_PROVIDERS, 1)]}
    except (OSError, ValueError) as error:
        raise RuntimeError('Historique PLLM illisible ou invalide ; fichier préservé') from error
    if not isinstance(data, dict) or not isinstance(data.get('models'), list):
        raise RuntimeError('Historique PLLM invalide : politiques attendues ; fichier préservé')
    version = data.get('schema_version', 1)
    providers = ('opencodego', 'opencodego', 'openrouter', 'deepseek') if version == 1 else POLICY_PROVIDERS
    if version not in (1, 2) or len(data['models']) != len(providers):
        raise RuntimeError('Historique PLLM invalide : schéma ou nombre de politiques ; fichier préservé')
    models = data['models']
    for priority, provider in enumerate(providers, 1):
        matches = [m for m in models if isinstance(m, dict) and m.get('mode') == f'mode{priority}']
        if (len(matches) != 1 or matches[0].get('priority') != priority
                or matches[0].get('provider') not in ((provider, 'opencode') if provider == 'opencodego' else (provider,))
                or not isinstance(matches[0].get('condition'), str)
                or not isinstance(matches[0].get('reasoning'), str)
                or matches[0].get('state') not in ('Valide', 'Invalide')
                or ('model' in matches[0] and not isinstance(matches[0]['model'], str))):
            raise RuntimeError('Historique PLLM invalide : politiques incohérentes ; fichier préservé')
        matches[0].setdefault('model', matches[0].get('model_id') or 'Non évalué')
    if version == 1:
        for model in models:
            priority = {'mode3': 5, 'mode4': 6}.get(model['mode'], model['priority'])
            model.update(mode=f'mode{priority}', priority=priority, selected=False, evaluated_this_run=False)
        models.extend(initial_model(priority, 'opencodego') for priority in (3, 4))
        models.sort(key=lambda model: model['priority'])
        data.update(schema_version=2, migrated_from_schema_version=1,
                    selected_mode=None, selection_status='no_valid_model')
    return data


def resource_category(model, key):
    if model['mode'] in FREE_MODES:
        model.update(quotas=None, quota_status='not_applicable')
        return 'free'
    try:
        quota(model, key)
    except QuotaExhausted:
        model['quota_status'] = 'exhausted'
        raise
    except Exception:
        model['quota_status'] = 'unavailable'
        raise
    model['quota_status'] = 'checked'
    return 'paid'


def check_category(model, key, category):
    current = resource_category(model, key)
    if current != category:
        raise CategoryChanged(current)


def catalog_candidate(row, section, rank, generated_at):
    if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
        raise RuntimeError('Candidat TFL sans identifiant vérifiable')
    if row.get('context_length', 0) < 1_000_000:
        raise RuntimeError('Contexte TFL inférieur à 1M ou non vérifiable')
    if set(row.get('output_modalities') or []) & {'audio', 'video', 'speech', 'sound'}:
        raise RuntimeError('Sortie TFL non admissible')
    if row['id'] in ('muse-spark-1.2-contributor', 'meta/muse-spark-1.2-contributor'):
        raise RuntimeError('Blacklist TFL permanente')
    if section == 'openrouter':
        prices = (finite(row['input_price']), finite(row['output_price']))
        provider = 'openrouter'
        endpoint, protocol = 'https://openrouter.ai/api/v1/chat/completions', 'chat_completions'
    else:
        if row.get('available') is not True:
            raise RuntimeError('Candidat TFL indisponible')
        reference = row['reference_pricing_usd_per_million_tokens']
        keys = ('input_off_peak', 'output_off_peak') if section == 'opencode_go' else ('input', 'output')
        prices = tuple(finite(reference[k]) for k in keys)
        provider = 'opencodego' if section == 'opencode_go' else 'opencode'
        endpoint, protocol = row.get('api_endpoint'), row.get('api_protocol')
        if protocol not in ('responses', 'chat_completions', 'messages') or not isinstance(endpoint, str):
            raise RuntimeError('Routage TFL absent ou protocole non benchmarké')
        url = urlsplit(endpoint)
        if (url.scheme != 'https' or url.hostname != 'opencode.ai' or url.port not in (None, 443)
                or url.username or url.password or url.query or url.fragment):
            raise RuntimeError('Origine du routage TFL non autorisée')
    if any(price < 0 for price in prices) or not math.isfinite(sum(prices)) or sum(prices) / 2 > 0.5:
        raise RuntimeError('Prix TFL hors critères ou non vérifiable')
    free = performance.is_free(row, section)
    average_price = float(sum(Decimal(str(price)) for price in prices) / 2)
    return {'model_id': row['id'], 'model': row.get('name') or row['id'], 'provider': provider,
            'api_endpoint': endpoint, 'api_protocol': protocol,
            'throughput_scope': 'reasoning_and_response' if section != 'openrouter' else 'response_only',
            'average_price_usd_per_million_tokens': average_price,
            'is_free': free, 'reasoning_capabilities': performance.capabilities(row), 'model_source': {'selector': 'tfl_order_first_success' if free else 'tfl_price_first_success', 'section': section,
                                             'rank': rank, 'generated_at': generated_at,
                                             'input_price_usd_per_million_tokens': prices[0],
                                             'output_price_usd_per_million_tokens': prices[1]}}


def candidates_for(model, category, catalog_path, forced=None):
    if ((model['mode'] in FREE_MODES and category != 'free')
            or (model['mode'] in ('mode1', 'mode2', 'mode5', 'mode6') and category != 'paid')):
        raise RuntimeError('Catégorie incompatible avec la politique PLLM')
    if model['mode'] == 'mode6':
        return [{'model_id': 'deepseek-v4-flash', 'model': 'deepseek-v4-flash',
                 'provider': 'deepseek', 'throughput_scope': 'response_only',
                 'api_protocol': 'chat_completions', 'api_endpoint': 'https://api.deepseek.com/chat/completions',
                 'is_free': False}]
    catalog = load_tfl_catalog(catalog_path)
    go = model['mode'] in ('mode1', 'mode2', *FREE_MODES)
    sections = ('opencode_go', 'opencode') if model['mode'] in FREE_MODES else (
        ('opencode_go',) if go else ('openrouter',))
    candidates = []
    for section in sections:
        source = catalog.get(section)
        if section == 'opencode' and source is None:
            continue
        rows = source.get('models') if isinstance(source, dict) else None
        if not isinstance(rows, list):
            raise RuntimeError('Section TFL absente ou invalide : ' + section)
        requested = forced.get('rank') if forced and model['mode'] not in FREE_MODES else None
        if requested is not None and (requested < 1 or requested > len(rows)):
            raise RuntimeError('Rang TFL indisponible : ' + str(requested))
        for rank, row in enumerate(rows, 1):
            if requested is not None and rank != requested:
                continue
            try:
                candidate = catalog_candidate(row, section, rank, catalog.get('generated_at'))
            except (KeyError, TypeError, ValueError, RuntimeError) as error:
                if forced and requested is not None:
                    raise RuntimeError('Candidat forcé non admissible : ' + error_message(error)) from error
                model['candidate_exclusions'].append({'section': section, 'rank': rank, 'cause': error_message(error)})
                continue
            if candidate['is_free'] != (category == 'free'):
                if forced and requested is not None:
                    raise RuntimeError('Candidat forcé incompatible avec les ressources : catégorie ' + category)
                continue
            candidates.append(candidate)
    if forced and model['mode'] in FREE_MODES:
        rank = forced.get('rank', 1)
        if rank < 1 or rank > len(candidates):
            raise RuntimeError('Rang gratuit TFL indisponible : ' + str(rank))
        return [candidates[rank - 1]]
    if not forced and category == 'paid':
        candidates.sort(key=lambda candidate: candidate['average_price_usd_per_million_tokens'])
    return candidates[:1] if forced else candidates


def evaluate_candidate(model, key, category, memory, session_id):
    attempts = []
    stage = 'configuration du test'
    model.update(throughput_metric=performance.THROUGHPUT_METRIC, throughput_window=performance.THROUGHPUT_WINDOW,
                 measurement_protocol_version=performance.MEASUREMENT_PROTOCOL_VERSION)
    try:
        metadata = {'reasoning_capabilities': model.get('reasoning_capabilities', {})}
        if model['provider'] == 'openrouter':
            metadata = next((item for item in get('https://openrouter.ai/api/v1/models', key)['data']
                             if item['id'] == model['model_id']), None)
            if metadata is None:
                raise RuntimeError('Modèle absent des métadonnées OpenRouter actuelles')
        performance.reasoning(model, BUDGETS[0], metadata)
        ttft_limit, throughput_limit = performance_limits(model)
        model['performance_criteria'] = {'ttft_lt_seconds': ttft_limit, 'tokens_per_second_gt': throughput_limit}
        model['condition'] = f'TTFT < {ttft_limit} s ET tokens/s > {throughput_limit} ET contrôles applicables'
        pending = list(budgets_for(model, memory))
        while pending:
            budget = pending.pop(0)
            stage = 'quotas avant performance'
            check_category(model, key, category)
            stage = 'performance'
            model.update(ttft_seconds=None, tokens_per_second=None,
                         performance_test={'status': 'not_run', 'max_tokens': budget, 'requests': 0, 'reasoning': model.get('reasoning', 'high')})
            try:
                try:
                    complete = benchmark(model, key, budget, metadata, session_id=session_id)
                except (urllib.error.HTTPError, ApiFailure) as error:
                    diagnostic = http_diagnostic(error)
                    if not performance.can_retry_xhigh(model, metadata, diagnostic):
                        raise
                    attempts.append({**copy.deepcopy(model['performance_test']), 'status': 'failed',
                                     'http_error': copy.deepcopy(diagnostic), 'reasoning': 'high'})
                    model['reasoning'] = 'xhigh'
                    pending = list(budgets_for(model, memory))
                    budget = pending.pop(0)
                    check_category(model, key, category)
                    complete = benchmark(model, key, budget, metadata, session_id=session_id)
                if not complete:
                    raise RuntimeError('Budget du test épuisé : mesure inconclusive')
                ttft = finite(model['ttft_seconds'])
                throughput = finite(model['tokens_per_second'])
                ttft_limit, throughput_limit = performance_limits(model)
                if ttft < 0 or ttft >= ttft_limit or throughput <= throughput_limit:
                    raise RuntimeError('Seuil de performance non satisfait')
                model.update(ttft_seconds=ttft, tokens_per_second=throughput,
                             performance_criteria={'ttft_lt_seconds': ttft_limit, 'tokens_per_second_gt': throughput_limit})
                model['condition'] = f'TTFT < {ttft_limit} s ET tokens/s > {throughput_limit} ET contrôles applicables'
            except Exception as error:
                model['performance_test'].update(status='failed', reason=error_message(error), model_id=model['model_id'])
                if isinstance(error, (urllib.error.HTTPError, ApiFailure)):
                    model['performance_test']['http_error'] = copy.deepcopy(http_diagnostic(error))
                attempts.append(copy.deepcopy(model['performance_test']))
                if is_authentication_error(error):
                    raise AuthenticationFailure(error_message(error)) from error
                if (isinstance(error, (urllib.error.HTTPError, ApiFailure))
                        and http_diagnostic(error)['http_status'] in (400, 403, 429)):
                    raise
                if budget == BUDGETS[-1]:
                    raise
                continue
            model['performance_test']['model_id'] = model['model_id']
            attempts.append(copy.deepcopy(model['performance_test']))
            remember_success(model, budget, memory)
            model.update(state='Valide', cause='Tous les critères satisfaits')
            break
        else:
            raise RuntimeError('Aucune mesure concluante après épuisement des paliers')
    except CategoryChanged:
        raise
    except Exception as error:
        model.update(state='Invalide', cause=stage + ' : ' + error_message(error))
        if is_authentication_error(error):
            raise AuthenticationFailure(error_message(error)) from error
        if stage == 'quotas avant performance':
            raise ResourceFailure(model['cause']) from error
        model['performance_test'].update(reason=model['cause'])
    finally:
        model['performance_test']['attempts'] = attempts
    return model


def main(active=False, forced=None, tfl_catalog=None):
    signal.signal(signal.SIGALRM, expire)
    data = load_current()
    memory = load_memory()
    data['models'].sort(key=lambda model: model['priority'])
    if [model['mode'] for model in data['models']] != [f'mode{i}' for i in range(1, 7)]:
        raise RuntimeError('Ce protocole attend les six modes définis')
    data['evaluation_mode'] = 'active' if active else ('forced' if forced else 'all')
    if forced:
        data['forced_policy'] = {'mode': forced['mode'], 'rank': forced.get('rank')}
    else:
        data.pop('forced_policy', None)
    for model in data['models']:
        model.update(evaluated_this_run=False, selected=False)
    for model, provider, secret_policy, account_index in zip(
            data['models'], POLICY_PROVIDERS, SECRET_POLICIES, SECRET_ACCOUNT_INDICES):
        if forced and model['mode'] != forced['mode']:
            continue
        model.update(evaluated_this_run=True, state='Invalide', cause='', selected=False,
                     provider=provider, model='Non évalué', model_id='Non évalué', reasoning='high',
                     ttft_seconds=None, tokens_per_second=None, quotas=None, evaluated_at=now(),
                     last_successful_max_tokens=None, selection_category=None,
                     throughput_metric=performance.THROUGHPUT_METRIC, throughput_window=performance.THROUGHPUT_WINDOW,
                     measurement_protocol_version=performance.MEASUREMENT_PROTOCOL_VERSION,
                     candidate_results=[], candidate_exclusions=[],
                     condition=initial_model(model['priority'], provider)['condition'],
                     performance_criteria=initial_model(model['priority'], provider)['performance_criteria'],
                     quota_status='not_applicable' if model['mode'] in FREE_MODES else 'not_evaluated',
                     performance_test={'status': 'not_run', 'reason': 'Contrôle des ressources requis'})
        for field in ('quotas_evaluated_at', 'quota_provider', 'api_endpoint', 'api_protocol', 'model_source', 'is_free',
                      'average_price_usd_per_million_tokens'):
            model.pop(field, None)
        key = ''
        try:
            secret = subprocess.run(['secret-tool', 'lookup', 'service', 'pllm', 'policy', secret_policy,
                                     'provider', provider, 'account', ACCOUNTS[account_index]], capture_output=True, timeout=15)
            if secret.returncode or not secret.stdout.strip():
                raise AuthenticationFailure('Clé API inaccessible dans le trousseau')
            key = secret.stdout.decode().strip()
            category = resource_category(model, key)
            session_id = str(uuid.uuid4()) if provider == 'opencodego' else None
            for transition in range(3):
                model['selection_category'] = category
                candidates = candidates_for(model, category, tfl_catalog, forced=forced)
                if not candidates:
                    raise RuntimeError('Aucun candidat TFL admissible ' + ('gratuit' if category == 'free' else 'payant'))
                results = []
                try:
                    for candidate in candidates:
                        current = {k: copy.deepcopy(v) for k, v in model.items()
                                   if k not in ('candidate_results', 'candidate_exclusions')}
                        current.update(candidate)
                        current.update(state='Invalide', cause='', last_successful_max_tokens=None,
                                       evaluated_at=now(), ttft_seconds=None, tokens_per_second=None,
                                       performance_test={'status': 'not_run', 'reason': 'Test non exécuté'})
                        try:
                            evaluate_candidate(current, key, category, memory, session_id)
                        except (CategoryChanged, AuthenticationFailure, ResourceFailure):
                            records = model['candidate_results']
                            records.append(copy.deepcopy(current))
                            model.update(current)
                            model['candidate_results'] = records
                            raise
                        results.append(current)
                        model['candidate_results'].append(copy.deepcopy(current))
                        model['quotas'] = current['quotas']
                        model['quotas_evaluated_at'] = current.get('quotas_evaluated_at')
                        if current['state'] == 'Valide':
                            break
                except CategoryChanged as error:
                    if forced or transition == 2:
                        raise RuntimeError('Ressources modifiées pendant les tests ; nouvelle évaluation requise') from error
                    category = error.category
                    continue
                valid = [result for result in results if result['state'] == 'Valide']
                winner = valid[0] if valid else results[-1]
                records, exclusions = model['candidate_results'], model['candidate_exclusions']
                quotas, quota_time = model['quotas'], model.get('quotas_evaluated_at')
                model.update(winner)
                model.update(candidate_results=records, candidate_exclusions=exclusions,
                             quotas=quotas, quotas_evaluated_at=quota_time)
                break
        except Exception as error:
            model.update(state='Invalide', cause=error_message(error), ttft_seconds=None, tokens_per_second=None)
            status = 'not_run' if model['performance_test']['status'] == 'not_run' else 'failed'
            model['performance_test'].update(status=status, reason=model['cause'])
            if isinstance(error, (urllib.error.HTTPError, ApiFailure)):
                model['performance_test']['http_error'] = copy.deepcopy(http_diagnostic(error))
        finally:
            signal.alarm(0)
            key = ''
        if active and model['state'] == 'Valide':
            break
    publish(data, active=active, forced_mode=forced['mode'] if forced else None)


FORCED_COMMANDS = {
    '1': {'mode': 'mode1'},
    '11': {'mode': 'mode1', 'rank': 1},
    '12': {'mode': 'mode1', 'rank': 2},
    '13': {'mode': 'mode1', 'rank': 3},
    '2': {'mode': 'mode2'},
    '21': {'mode': 'mode2', 'rank': 1},
    '22': {'mode': 'mode2', 'rank': 2},
    '23': {'mode': 'mode2', 'rank': 3},
    '3': {'mode': 'mode3'},
    '31': {'mode': 'mode3', 'rank': 1},
    '32': {'mode': 'mode3', 'rank': 2},
    '33': {'mode': 'mode3', 'rank': 3},
    '4': {'mode': 'mode4'},
    '41': {'mode': 'mode4', 'rank': 1},
    '42': {'mode': 'mode4', 'rank': 2},
    '43': {'mode': 'mode4', 'rank': 3},
    '5': {'mode': 'mode5'},
    '51': {'mode': 'mode5', 'rank': 1},
    '52': {'mode': 'mode5', 'rank': 2},
    '53': {'mode': 'mode5', 'rank': 3},
    '6': {'mode': 'mode6'},
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', choices=['active', *FORCED_COMMANDS])
    parser.add_argument('--tfl-catalog', type=Path, help='Chemin explicite du catalogue TFL')
    args = parser.parse_args()
    forced = FORCED_COMMANDS.get(args.mode)
    main(active=args.mode == 'active', forced=forced, tfl_catalog=args.tfl_catalog)
