"""Mesures streaming communes PLLM/TFL, sans stockage de clé ni contrôle de quota."""
import json
import math
import re
import signal
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from http.client import HTTPException
from zoneinfo import ZoneInfo

PROMPT = 'Write only Python code for a stable merge_sort(values) function and three assert tests. No explanation.'
BUDGETS = (1024, 2048, 4096, 8192)
MEASUREMENT_PROTOCOL_VERSION = 8
THROUGHPUT_METRIC = 'request_average_v1'
THROUGHPUT_WINDOW = 'request_total'

FREE_CRITERIA = {'minimum_context_tokens': 1_000_000, 'ttft_lt_seconds': 30, 'tokens_per_second_gt': 20}

class AuthenticationFailure(RuntimeError):
    """Authentication failed; do not hide it behind another candidate."""

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


def limits(model):
    return (30, 20) if model.get('is_free') is True or model.get('mode') in ('mode3', 'mode4') else (90, 15)


def is_free(row, section):
    if section == 'openrouter':
        prices = (row.get('input_price'), row.get('output_price'))
    else:
        ref = row.get('reference_pricing_usd_per_million_tokens') or {}
        keys = ('input_off_peak', 'output_off_peak') if section == 'opencode_go' else ('input', 'output')
        prices = tuple(ref.get(key) for key in keys)
    try:
        if not all(value is not None and finite(value) == 0 for value in prices):
            return False
        if any(any(finite(variant[key]) != 0 for key in ('input', 'output')) for variant in row.get('pricing_variants') or []):
            return False
        details = row.get('pricing_details') or {}
        if any(name.endswith(('prompt', 'completion')) for name in details.get('unverified_fields', [])):
            return False
        for variant in details.get('overrides', []):
            if any(variant.get(key) is not None and finite(variant[key]) != 0 for key in ('prompt', 'completion')):
                return False
    except (KeyError, TypeError, ValueError):
        return False
    return True


def capabilities(*records):
    for record in records:
        if not isinstance(record, dict):
            continue
        options = record.get('reasoning_capabilities', record.get('reasoning'))
        if isinstance(options, dict):
            values = {key: options[key] for key in ('supported_efforts', 'supports_max_tokens') if key in options}
            if values:
                return values
        effort = record.get('effort')
        if isinstance(effort, dict) and isinstance(effort.get('supported_levels'), list):
            return {'supported_efforts': effort['supported_levels']}
    return {}


def choose_effort(model, metadata):
    options = capabilities(metadata)
    efforts = options.get('supported_efforts')
    if (efforts is not None and (not isinstance(efforts, list) or any(not isinstance(value, str) for value in efforts))
            or ('supports_max_tokens' in options and not isinstance(options['supports_max_tokens'], bool))):
        raise RuntimeError('Métadonnées de raisonnement invalides')
    requested = model.get('reasoning', 'high')
    if requested not in ('high', 'xhigh'):
        raise RuntimeError('Raisonnement autorisé : HIGH ou XHIGH uniquement')
    if isinstance(efforts, list) and requested not in efforts:
        if requested == 'high' and 'xhigh' in efforts:
            requested = 'xhigh'
        elif not options.get('supports_max_tokens'):
            raise RuntimeError('HIGH et XHIGH non pris en charge dans les métadonnées')
    model.update(requested_reasoning='high', reasoning=requested)
    return requested


def reasoning(model, budget, metadata):
    effort = choose_effort(model, metadata)
    if model['provider'] in ('opencodego', 'opencode'):
        protocol = model.get('api_protocol', 'chat_completions')
        if protocol == 'responses':
            return {'reasoning': {'effort': effort}}
        if protocol == 'messages':
            return {'thinking': {'type': 'adaptive'}, 'output_config': {'effort': effort}}
        if protocol == 'chat_completions':
            return {'reasoning_effort': effort}
        raise RuntimeError('Protocole API OpenCode non pris en charge')
    if model['provider'] == 'deepseek':
        return {'reasoning_effort': effort, 'thinking': {'type': 'enabled'}}
    options = capabilities(metadata)
    efforts = options.get('supported_efforts')
    if (isinstance(efforts, list) and effort in efforts) or ('supported_efforts' in options and efforts is None):
        return {'reasoning': {'effort': effort}}
    if options.get('supports_max_tokens') is True:
        return {'reasoning': {'max_tokens': budget * (95 if effort == 'xhigh' else 80) // 100}}
    raise RuntimeError('HIGH et XHIGH non pris en charge dans les métadonnées OpenRouter')


def can_retry_xhigh(model, metadata, diagnostic):
    return (model.get('reasoning') == 'high' and diagnostic.get('http_status') == 400
            and diagnostic.get('parameter') in ('reasoning_effort', 'reasoning.effort', 'output_config.effort')
            and 'xhigh' in (capabilities(metadata).get('supported_efforts') or []))

def run_benchmark(m, key, budget, metadata, session_id=None, *, reasoning, request, now, api_error, clock, alarm):
    m.update(ttft_seconds=None, tokens_per_second=None, throughput_metric=THROUGHPUT_METRIC,
             throughput_window=THROUGHPUT_WINDOW, measurement_protocol_version=MEASUREMENT_PROTOCOL_VERSION)
    options = reasoning(m, budget, metadata)
    protocol = m.get('api_protocol', 'chat_completions')
    result = {'status': 'running', 'prompt': PROMPT, 'max_tokens': budget, 'reasoning_request': options,
              'started_at': now(), 'ttft_target': 'content (hors raisonnement)', 'requests': 1,
              'api_protocol': protocol, 'api_endpoint': m.get('api_endpoint'),
              'reasoning': m['reasoning'], 'requested_reasoning': 'high',
              'throughput_metric': THROUGHPUT_METRIC, 'throughput_window': THROUGHPUT_WINDOW,
              'measurement_protocol_version': MEASUREMENT_PROTOCOL_VERSION}
    if m['provider'] in ('opencodego', 'opencode'):
        result['session_header'] = 'x-opencode-session'
    m['performance_test'] = result
    url = m.get('api_endpoint') if m['provider'] in ('opencodego', 'opencode') else {'openrouter': 'https://openrouter.ai/api/v1/chat/completions', 'deepseek': 'https://api.deepseek.com/chat/completions'}[m['provider']]
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
    if protocol == 'messages':
        body.pop('stream_options', None)
    extra_headers = None
    if m['provider'] in ('opencodego', 'opencode'):
        extra_headers = {'Accept': 'text/event-stream'}
        if protocol == 'messages':
            extra_headers['x-api-key'] = key
        if session_id:
            extra_headers['x-opencode-session'] = session_id
    start = clock()
    first = last = first_reason = first_generated = last_generated = None
    usage = None
    done = False
    alarm(120)
    try:
        with request(url, key, body, extra_headers=extra_headers) as response:
            for line in response:
                tick = clock()
                if not line.startswith(b'data:'):
                    continue
                raw = line[5:].strip()
                if raw == b'[DONE]':
                    done = True
                    break
                event = json.loads(raw)
                if event.get('error'):
                    error = event['error']
                    raise api_error(error.get('code') or error.get('type'), error) if isinstance(error, dict) else api_error(None)
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
                        raise api_error(event.get('code'), event)
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
        alarm(0)
        finished = clock()
        elapsed = finished - start
        elapsed = elapsed if math.isfinite(elapsed) else None
        result['request_seconds'] = elapsed
        result['duration_seconds'] = None if elapsed is None else round(elapsed, 4)
        for field, tick in (('ttft_reasoning_seconds', first_reason), ('ttft_seconds', first)):
            delay = None if tick is None else tick - start
            if (delay is None or not math.isfinite(delay) or elapsed is None or elapsed <= 0
                    or delay < 0 or delay > elapsed):
                delay = None
            value = None if delay is None else round(delay, 4)
            if field == 'ttft_seconds':
                m[field] = value
            else:
                result[field] = value
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
    if elapsed is None or elapsed <= 0:
        raise RuntimeError('Durée totale de requête invalide : débit non mesurable')
    if m['ttft_seconds'] is None:
        raise RuntimeError('Horodatage du contenu invalide : débit non mesurable')
    n = result.get('completion_tokens')
    rn = result.get('reasoning_tokens')
    if type(n) is not int or n <= 1:
        raise RuntimeError('Comptage des tokens indisponible')
    if m['provider'] in ('opencodego', 'opencode'):
        count = n
        begin, end = first_generated, last_generated
        m['throughput_scope'] = 'reasoning_and_response'
        result['throughput_formula'] = 'completion_tokens / request_seconds'
    else:
        if ((first_reason is not None and rn is None)
                or (rn is not None and (type(rn) is not int or rn < 0 or rn > n))):
            raise RuntimeError('Comptage distinct des tokens indisponible ou incohérent')
        count = n - (rn or 0)
        begin, end = first, last
        m['throughput_scope'] = 'response_only'
        result['throughput_formula'] = '(completion_tokens - reasoning_tokens) / request_seconds'
    if (count <= 1 or begin is None or end is None or not math.isfinite(begin)
            or not math.isfinite(end) or begin < start or end < begin or end > finished):
        raise RuntimeError('Échantillon de génération insuffisant ou incohérent')
    # La fenêtre entre fragments reste un diagnostic ; un bloc unique peut donner une durée nulle.
    result['generation_seconds'] = round(end - begin, 4)
    result['throughput_scope'] = m['throughput_scope']
    try:
        rate = count / elapsed
    except OverflowError as error:
        raise RuntimeError('Débit non fini : mesure inexploitable') from error
    if not math.isfinite(rate):
        raise RuntimeError('Débit non fini : mesure inexploitable')
    m['tokens_per_second'] = round(rate, 3)
    result['status'] = 'completed'
    return True

def benchmark(model, key, budget, metadata, session_id=None):
    return run_benchmark(model, key, budget, metadata, session_id,
                         reasoning=reasoning, request=request, now=now, api_error=api_error,
                         clock=time.monotonic, alarm=signal.alarm)
