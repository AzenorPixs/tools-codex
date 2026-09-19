#!/usr/bin/env python3
"""Evaluate PLLM quotas before bounded streaming benchmarks; publish no secrets."""
import json
import argparse
import math
import signal
import subprocess
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = 'Write only Python code for a stable merge_sort(values) function and three assert tests. No explanation.'
BUDGETS = (1024, 2048, 4096, 8192)
MEMORY_PATH = ROOT / 'data/pllm-performance-memory.json'

OPENCODE_GO_ROUTE_BY_MODEL = {
    'muse-spark-1.3-contributor': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
    'muse-spark-1.2-contributor': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
    'gpt-5.6-luna': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
    'grok-4.6': ('https://opencode.ai/zen/go/v1/responses', 'responses'),
}

ACCOUNTS = ['anthony.demard44@gmail.com', 'az.github@pixs.fr', 'az.openrouter@pixs.fr', 'az.deepseek@pixs.fr']


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
    if m['provider'] == 'opencodego':
        q = get('https://opencode.ai/zen/go/v1/usage', key)['usage']
        m['quotas'] = q
        failed = [p for p in ['rolling', 'weekly', 'monthly'] if finite(q[p]['percent']) >= 100 or q[p]['status'] != 'ok']
        if failed:
            raise RuntimeError('Quota indisponible : ' + ', '.join(failed))
    elif m['provider'] == 'openrouter':
        q = get('https://openrouter.ai/api/v1/credits', key)['data']
        balance = finite(q['total_credits']) - finite(q['total_usage'])
        m['quotas'] = {'balance': balance, 'currency': 'USD'}
        if balance <= 0:
            raise RuntimeError('Solde épuisé')
    else:
        q = get('https://api.deepseek.com/user/balance', key)
        m['quotas'] = q
        if q['is_available'] is not True or not any(finite(b['total_balance']) > 0 for b in q['balance_infos']):
            raise RuntimeError('Solde indisponible ou épuisé')
    m['quotas_evaluated_at'] = now()


def reasoning(m, budget, metadata):
    if m['provider'] == 'opencodego':
        if m.get('api_protocol') == 'responses':
            return {'reasoning': {'effort': 'low'}}
        if m.get('api_protocol') == 'messages':
            return {'thinking': {'type': 'enabled', 'budget_tokens': budget // 5}}
    if m['provider'] != 'openrouter':
        return {'reasoning_effort': 'low', 'thinking': {'type': 'enabled'}}
    options = metadata.get('reasoning') or {}
    efforts = options.get('supported_efforts')
    if ('supported_efforts' in options and efforts is None) or (isinstance(efforts, list) and 'low' in efforts):
        return {'reasoning': {'effort': 'low'}}
    if options.get('supports_max_tokens') is True:
        return {'reasoning': {'max_tokens': budget // 5}}
    raise RuntimeError('Low non pris en charge dans les métadonnées OpenRouter')


def benchmark(m, key, budget, metadata, session_id=None):
    options = reasoning(m, budget, metadata)
    protocol = m.get('api_protocol', 'chat_completions')
    result = {'status': 'running', 'prompt': PROMPT, 'max_tokens': budget, 'reasoning_request': options,
              'started_at': now(), 'ttft_target': 'content (hors raisonnement)', 'requests': 1,
              'api_protocol': protocol, 'api_endpoint': m.get('api_endpoint')}
    if m['provider'] == 'opencodego':
        result['session_header'] = 'x-opencode-session'
    m['performance_test'] = result
    url = m.get('api_endpoint') if m['provider'] == 'opencodego' else {'openrouter': 'https://openrouter.ai/api/v1/chat/completions', 'deepseek': 'https://api.deepseek.com/chat/completions'}[m['provider']]
    if not url:
        raise RuntimeError('Point d’accès API du modèle OpenCode Go absent du catalogue TFL')
    model_id = m['model_id']
    if protocol == 'responses':
        body = {'model': model_id,
                'input': [{'role': 'user', 'content': [{'type': 'input_text', 'text': PROMPT}]}],
                'max_output_tokens': budget, 'stream': True, 'store': False, **options}
    else:
        body = {'model': model_id, 'messages': [{'role': 'user', 'content': PROMPT}], 'max_tokens': budget,
                'stream': True, 'stream_options': {'include_usage': True}, **options}
    extra_headers = None
    if m['provider'] == 'opencodego':
        extra_headers = {'Accept': 'text/event-stream'}
        if protocol == 'messages':
            extra_headers['x-api-key'] = key
        if session_id:
            extra_headers['x-opencode-session'] = session_id
    start = time.monotonic()
    first = last = first_reason = first_generated = last_generated = None
    usage = None
    done = False
    signal.alarm(120)
    try:
        with request(url, key, body, extra_headers=extra_headers) as response:
            for line in response:
                tick = time.monotonic()
                if not line.startswith(b'data:'):
                    continue
                raw = line[5:].strip()
                if raw == b'[DONE]':
                    done = True
                    break
                event = json.loads(raw)
                if event.get('error'):
                    raise RuntimeError('Erreur dans le flux API')
                if protocol == 'messages':
                    event_type = event.get('type')
                    delta = event.get('delta') or {}
                    delta_type = delta.get('type')
                    if delta_type in ('thinking_delta', 'signature_delta', 'text_delta'):
                        text = delta.get('thinking') if delta_type == 'thinking_delta' else delta.get('text')
                        if text:
                            if first_generated is None:
                                first_generated = tick
                            last_generated = tick
                            if delta_type == 'thinking_delta':
                                if first_reason is None:
                                    first_reason = tick
                            elif first is None:
                                first = tick
                            if delta_type == 'text_delta':
                                last = tick
                    if event_type == 'message_start':
                        usage = (event.get('message') or {}).get('usage') or usage
                    if event_type == 'message_delta':
                        usage = event.get('usage') or usage
                        stop_reason = delta.get('stop_reason')
                        if stop_reason:
                            result['finish_reason'] = 'stop' if stop_reason in ('end_turn', 'stop') else stop_reason
                    if event_type == 'message_stop':
                        done = True
                        break
                    continue
                if protocol == 'responses':
                    event_type = event.get('type')
                    if event_type in ('response.output_text.delta', 'response.reasoning_text.delta',
                                      'response.reasoning_summary_text.delta'):
                        delta = event.get('delta')
                        if delta:
                            if first_generated is None:
                                first_generated = tick
                            last_generated = tick
                            if event_type == 'response.output_text.delta':
                                if first is None:
                                    first = tick
                                last = tick
                            elif first_reason is None:
                                first_reason = tick
                    if event_type == 'response.completed':
                        response = event.get('response') or {}
                        usage = response.get('usage')
                        result['finish_reason'] = 'stop' if response.get('status') == 'completed' else 'length'
                        done = True
                        break
                    if event_type == 'error':
                        raise RuntimeError('Erreur dans le flux API')
                    continue
                if event.get('provider'):
                    result['upstream_provider'] = event['provider']
                if event.get('usage'):
                    usage = event['usage']
                for choice in event.get('choices', []):
                    delta = choice.get('delta', {})
                    if delta.get('content') or delta.get('reasoning') or delta.get('reasoning_content'):
                        if first_generated is None:
                            first_generated = tick
                        last_generated = tick
                    if (delta.get('reasoning') or delta.get('reasoning_content') or delta.get('reasoning_details')) and first_reason is None:
                        first_reason = tick
                    if delta.get('content'):
                        if first is None:
                            first = tick
                        last = tick
                    if choice.get('finish_reason'):
                        result['finish_reason'] = choice['finish_reason']
    finally:
        signal.alarm(0)
        result['duration_seconds'] = round(time.monotonic() - start, 4)
        result['ttft_reasoning_seconds'] = None if first_reason is None else round(first_reason - start, 4)
        m['ttft_seconds'] = None if first is None else round(first - start, 4)
    if usage:
        if protocol in ('responses', 'messages'):
            result['completion_tokens'] = usage.get('output_tokens')
            result['reasoning_tokens'] = (usage.get('output_tokens_details') or {}).get('reasoning_tokens')
        else:
            result['completion_tokens'] = usage.get('completion_tokens')
            result['reasoning_tokens'] = (usage.get('completion_tokens_details') or {}).get('reasoning_tokens')
    if result.get('finish_reason') == 'length':
        result['status'] = 'truncated'
        return False
    if protocol == 'messages' and result.get('finish_reason') is None and done:
        result['finish_reason'] = 'stop'
    if not done or result.get('finish_reason') != 'stop' or first is None:
        raise RuntimeError('Réponse absente ou flux incomplet')
    n = result.get('completion_tokens')
    rn = result.get('reasoning_tokens')
    if not isinstance(n, int) or n <= 1:
        raise RuntimeError('Comptage des tokens indisponible')
    if m['provider'] == 'opencodego':
        count = n
        begin, end = first_generated, last_generated
        m['throughput_scope'] = 'reasoning_and_response'
        result['throughput_formula'] = '(completion_tokens - 1) / (last_generated_time - first_generated_time)'
    else:
        if first_reason is not None and not isinstance(rn, int):
            raise RuntimeError('Comptage distinct des tokens indisponible')
        count = n - (rn or 0)
        begin, end = first, last
        m['throughput_scope'] = 'response_only'
        result['throughput_formula'] = '(completion_tokens - reasoning_tokens - 1) / (last_content_time - first_content_time)'
    if count <= 1 or begin is None or end is None or end <= begin:
        raise RuntimeError('Échantillon de génération insuffisant')
    result['generation_seconds'] = round(end - begin, 4)
    result['throughput_scope'] = m['throughput_scope']
    m['tokens_per_second'] = round((count - 1) / (end - begin), 3)
    result['status'] = 'completed'
    return True


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
    q = m.get('quotas')
    if not q:
        return {'text': '⚪ Non disponible', 'items': []}
    items = []
    if m['provider'] == 'opencodego':
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


def performance_color(metric, value):
    if value is None:
        return '⚪'
    if metric == 'ttft':
        if value < 30:
            return '🟢'
        if value < 45:
            return '🟡'
        if value < 60:
            return '🟠'
        return '🔴'
    if value > 30:
        return '🟢'
    if value >= 20:
        return '🟡'
    if value > 15:
        return '🟠'
    return '🔴'


def performance_display(metric, value, scope=None):
    if value is None:
        return '-'
    symbol = performance_color(metric, value)
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
            performance_display('ttft', model.get('ttft_seconds')),
            performance_display('tokens', model.get('tokens_per_second'), model.get('throughput_scope')),
            '🟢 Valide' if model['state'] == 'Valide' else '🔴 Invalide',
            model.get('last_successful_max_tokens') or '-',
            display_timestamp(model.get('evaluated_at')),
        ]
        lines.append('| ' + ' | '.join(markdown_text(value) for value in values) + ' |')
    return '\n'.join(['### Rapport PLLM', '', *lines])


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
             selection_status='selected' if chosen else 'no_valid_model', protocol_version=5)
    d.pop('last_partial_evaluation_at', None)
    if forced_mode:
        models = [m for m in d['models'] if m.get('evaluated_this_run') and m['mode'] == forced_mode]
    else:
        models = [chosen] if active and chosen else ([] if active else d['models'])
    if models:
        content = policy_table(models) + '\n\n' + quota_summary(models) + '\n\n' + active_summary(d['models']) + '\n'
    else:
        content = '**Aucune politique valide**\n'
    for name, output in [('pllm-current.json', json.dumps(d, ensure_ascii=False, indent=2) + '\n'), ('pllm-current.md', content)]:
        p = ROOT / 'data' / name
        temp = p.with_name(p.name + '.tmp')
        temp.write_text(output, encoding='utf-8')
        temp.replace(p)
    if not active:
        print(content, flush=True)


def tfl_opencode_model_at(rank):
    catalog_path = ROOT.parent / 'tfl/data/tfl.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    models = catalog.get('opencode_go', {}).get('models')
    if not isinstance(models, list) or not models:
        raise RuntimeError('Catalogue TFL OpenCode Go vide ou invalide')
    if not isinstance(rank, int) or rank < 1 or rank > len(models):
        raise RuntimeError(f'Rang OpenCode Go TFL indisponible : {rank}')
    model = models[rank - 1]
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


def next_tfl_opencode_model(current_id):
    catalog_path = ROOT.parent / 'tfl/data/tfl.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    models = catalog.get('opencode_go', {}).get('models')
    if not isinstance(models, list):
        return None
    found = False
    for candidate in models:
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
        return {'schema_version': 1, 'policies': {}}
    memory = json.loads(MEMORY_PATH.read_text(encoding='utf-8'))
    if memory.get('schema_version') != 1 or not isinstance(memory.get('policies'), dict):
        raise RuntimeError('Mémoire de performance PLLM invalide')
    return memory


def identity(m):
    return {k: m.get(k) for k in ('model_id', 'provider', 'reasoning', 'throughput_scope', 'api_protocol', 'api_endpoint')}


def budgets_for(m, memory):
    previous = memory['policies'].get(m['mode'], {})
    budget = previous.get('last_successful_max_tokens')
    if previous.get('identity') == identity(m) and budget in BUDGETS:
        m['last_successful_max_tokens'] = budget
        return BUDGETS[BUDGETS.index(budget):]
    m['last_successful_max_tokens'] = None
    return BUDGETS


def remember_success(m, budget, memory):
    memory['policies'][m['mode']] = {
        'identity': identity(m), 'last_successful_max_tokens': budget,
        'succeeded_at': now(), 'ttft_seconds': m['ttft_seconds'],
        'tokens_per_second': m['tokens_per_second'],
    }
    temp = MEMORY_PATH.with_name(MEMORY_PATH.name + '.tmp')
    temp.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(MEMORY_PATH)
    m['last_successful_max_tokens'] = budget


def main(active=False, forced=None):
    signal.signal(signal.SIGALRM, expire)
    memory = load_memory()
    d = json.loads((ROOT / 'data/pllm-current.json').read_text())
    d['models'].sort(key=lambda m: m['priority'])
    if [m['mode'] for m in d['models']] != ['mode1', 'mode2', 'mode3', 'mode4']:
        raise RuntimeError('Ce protocole attend les quatre modes définis')
    d['evaluation_mode'] = 'active' if active else ('forced' if forced else 'all')
    if forced:
        d['forced_policy'] = {'mode': forced['mode'], 'rank': forced.get('rank')}
    else:
        d.pop('forced_policy', None)
    for m in d['models']:
        m['evaluated_this_run'] = False
        m['selected'] = False
    for m, account in zip(d['models'], ACCOUNTS):
        if forced and m['mode'] != forced['mode']:
            continue
        m['evaluated_this_run'] = True
        m.update(state='Invalide', cause='', selected=False, ttft_seconds=None, tokens_per_second=None, quotas=None, evaluated_at=now(),
                 performance_test={'status': 'not_run', 'reason': 'Non exécuté — contrôle des quotas Invalide'})
        m['throughput_scope'] = 'reasoning_and_response' if m['provider'] == 'opencodego' else 'response_only'
        m.pop('quotas_evaluated_at', None)
        key = ''
        stage = 'quotas'
        try:
            r = subprocess.run(['secret-tool', 'lookup', 'service', 'pllm', 'policy', m['mode'], 'provider', m['provider'], 'account', account], capture_output=True, timeout=15)
            if r.returncode or not r.stdout.strip():
                raise RuntimeError('Secret inaccessible')
            key = r.stdout.decode().strip()
            stage = 'configuration du modèle'
            metadata = {}
            if m['provider'] == 'opencodego':
                rank = (forced.get('rank') or 1) if forced and forced['mode'] == m['mode'] else 1
                tfl_model, generated_at = tfl_opencode_model_at(rank)
                m['model_id'] = tfl_model['id']
                m['model'] = tfl_model.get('name') or m['model_id']
                m['api_endpoint'] = tfl_model['api_endpoint']
                m['api_protocol'] = tfl_model['api_protocol']
                m['model_source'] = {'selector': 'tfl_opencode_go_rank', 'rank': rank, 'generated_at': generated_at}
            elif m['provider'] == 'openrouter':
                catalog = json.loads((ROOT.parent / 'tfl/data/tfl.json').read_text())
                rank = (forced.get('rank') or 1) if forced and forced['mode'] == m['mode'] else 1
                openrouter_models = catalog['openrouter']['models']
                if not isinstance(rank, int) or rank < 1 or rank > len(openrouter_models):
                    raise RuntimeError(f'Rang OpenRouter TFL indisponible : {rank}')
                m['model_id'] = openrouter_models[rank - 1]['id']
                m['model'] = m['model_id']
                m['model_source'] = {'selector': 'tfl_openrouter_rank', 'rank': rank, 'generated_at': catalog['generated_at']}
            else:
                m['model_id'] = 'deepseek-v4-flash'
            stage = 'quotas'
            quota(m, key)
            stage = 'configuration du test'
            if m['provider'] == 'openrouter':
                metadata = next(x for x in get('https://openrouter.ai/api/v1/models', key)['data'] if x['id'] == m['model_id'])
            attempts = []
            session_id = str(uuid.uuid4()) if m['provider'] == 'opencodego' else None
            for budget in budgets_for(m, memory):
                if attempts:
                    stage = 'quotas avant nouvelle tentative'
                    quota(m, key)
                stage = 'performance'
                m['ttft_seconds'] = None
                m['tokens_per_second'] = None
                try:
                    complete = benchmark(m, key, budget, metadata, session_id=session_id)
                    if not complete:
                        raise RuntimeError('Budget du test épuisé : mesure inconclusive, pas une preuve de panne du modèle')
                    if m['ttft_seconds'] >= 60 or m['tokens_per_second'] <= 15:
                        raise RuntimeError('Seuil de performance non satisfait')
                except Exception as error:
                    message = ('HTTP 429 — rate_limit_exceeded (limitation fournisseur, test non concluant)' if isinstance(error, urllib.error.HTTPError) and error.code == 429 else 'HTTP ' + str(error.code) if isinstance(error, urllib.error.HTTPError) else str(error) if isinstance(error, RuntimeError) else type(error).__name__)
                    m['performance_test'].update(status='failed', reason=message)
                    attempts.append(dict(m['performance_test']))
                    m['performance_test']['attempts'] = list(attempts)
                    if (not forced and m['provider'] == 'opencodego' and m['mode'] in ('mode1', 'mode2')
                            and isinstance(error, urllib.error.HTTPError) and error.code == 429):
                        replacement = next_tfl_opencode_model(m['model_id'])
                        if replacement:
                            previous_model = m['model_id']
                            m['model_id'] = replacement['id']
                            m['model'] = replacement.get('name') or replacement['id']
                            m['api_endpoint'] = replacement['api_endpoint']
                            m['api_protocol'] = replacement['api_protocol']
                            m['model_source'] = {'selector': 'tfl_opencode_go_fallback_after_rate_limit',
                                                 'from_model': previous_model,
                                                 'generated_at': m.get('model_source', {}).get('generated_at')}
                            metadata = {}
                            m['performance_test']['fallback_model'] = replacement['id']
                            continue
                    if budget == BUDGETS[-1]:
                        raise
                    continue
                attempts.append(dict(m['performance_test']))
                m['performance_test']['attempts'] = list(attempts)
                remember_success(m, budget, memory)
                break
            m.update(state='Valide', cause='Tous les critères satisfaits')
        except Exception as e:
            message = ('HTTP 429 — rate_limit_exceeded (limitation fournisseur, test non concluant)' if isinstance(e, urllib.error.HTTPError) and e.code == 429 else 'HTTP ' + str(e.code) if isinstance(e, urllib.error.HTTPError) else str(e) if isinstance(e, RuntimeError) else type(e).__name__)
            m['cause'] = stage + ' : ' + message
            if m['performance_test']['status'] != 'not_run':
                m['performance_test'].update(status='failed', reason=message)
        finally:
            signal.alarm(0)
            key = ''
        if active and m['state'] == 'Valide':
            break
    publish(d, active=active, forced_mode=forced['mode'] if forced else None)


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
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', choices=['active', *FORCED_COMMANDS])
    args = parser.parse_args()
    forced = FORCED_COMMANDS.get(args.mode)
    main(active=args.mode == 'active', forced=forced)
