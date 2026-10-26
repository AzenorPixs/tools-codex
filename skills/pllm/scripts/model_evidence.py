"""Conclusions d'investigation du LLM, vérifiées sans inférence de modèle ou de route."""

from datetime import datetime
import hashlib
import ipaddress
import json
from pathlib import Path
import re
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

PROVIDERS = ('opencode_go', 'opencode', 'openrouter')
PROTOCOLS = ('chat_completions', 'responses', 'messages')
MAX_BYTES = 2_000_000


def timestamp():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def source_url(value):
    if not isinstance(value, str) or any(c.isspace() for c in value):
        raise RuntimeError('Preuve : URL de source invalide')
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme == 'https' and parsed.hostname and '.' in parsed.hostname
                 and parsed.username is None and parsed.password is None
                 and not parsed.query and not parsed.fragment and parsed.port in (None, 443))
        if parsed.hostname:
            try:
                ipaddress.ip_address(parsed.hostname)
            except ValueError:
                pass
            else:
                valid = False
    except ValueError as error:
        raise RuntimeError('Preuve : URL de source invalide') from error
    if not valid:
        raise RuntimeError('Preuve : source HTTPS publique requise')
    return value


def fetch_source(url, timeout):
    request = Request(source_url(url), headers={'Accept': 'text/html,text/markdown,application/json',
                                               'User-Agent': 'TFL/1.0'})
    with urlopen(request, timeout=timeout) as response:
        source_url(response.geturl())
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise RuntimeError('Preuve : source trop volumineuse')
    return raw


def validate_record(record):
    try:
        if (record['provider'] not in PROVIDERS or record['field'] not in ('context', 'reasoning')
                or not isinstance(record['model_id'], str) or not record['model_id']
                or record['status'] not in ('verified', 'unverifiable', 'unsupported')
                or not isinstance(record['conclusion'], str) or not record['conclusion'].strip()
                or datetime.fromisoformat(record['investigated_at']).tzinfo is None
                or not isinstance(record['sources'], list) or not record['sources']):
            raise ValueError('champ')
        if record['field'] == 'reasoning' and record.get('protocol') not in PROTOCOLS:
            raise ValueError('protocole')
        for source in record['sources']:
            source_url(source['url'])
            if (source.get('authority') != 'official'
                    or not re.fullmatch('[0-9a-f]{64}', source['sha256'])
                    or datetime.fromisoformat(source['retrieved_at']).tzinfo is None):
                raise ValueError('source')
        if record['status'] == 'verified':
            value = record['value']
            if record['field'] == 'context':
                if type(value) is not int or value <= 0:
                    raise ValueError('contexte')
            else:
                levels = value['supported_efforts']
                if (not isinstance(levels, list) or not levels
                        or any(not isinstance(level, str) for level in levels)
                        or not set(levels) & {'high', 'xhigh'}
                        or value.get('effort_equivalence') not in (None, 'thinking_enabled', 'accepted_alias')
                        or (value.get('effort_equivalence') == 'thinking_enabled'
                            and (record['provider'] == 'openrouter' or record['protocol'] != 'chat_completions'))):
                    raise ValueError('effort')
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError('Registre de preuves invalide : aucun contenu utilisateur affiché') from error


class EvidenceResolver:
    def __init__(self, paths=(), timeout=15, fetch=None):
        self.records = {}
        self.cache = {}
        self.timeout = timeout
        self.fetch = fetch_source if fetch is None else fetch
        for path in paths:
            path = Path(path)
            try:
                raw = path.read_bytes()
            except FileNotFoundError:
                continue
            except OSError as error:
                raise RuntimeError('Registre de preuves inaccessible') from error
            try:
                if len(raw) > MAX_BYTES:
                    raise ValueError('taille')
                data = json.loads(raw)
                if (type(data['schema_version']) is not int or data['schema_version'] != 1
                        or not isinstance(data['records'], list)):
                    raise ValueError('schema')
            except (KeyError, TypeError, ValueError, UnicodeError) as error:
                raise RuntimeError('Registre de preuves JSON invalide') from error
            local = set()
            for record in data['records']:
                validate_record(record)
                key = (record['provider'], record['model_id'], record['field'], record.get('protocol'))
                if key in local:
                    raise RuntimeError('Registre de preuves : déclaration dupliquée')
                local.add(key)
                self.records[key] = record

    def resolve(self, provider, model_id, field, protocol=None):
        result = {'provider': provider, 'model_id': model_id, 'field': field,
                  'protocol': protocol, 'status': 'required', 'checked_at': timestamp(),
                  'conclusion': 'Analyse et recherche du LLM requises dans les sources officielles.'}
        record = self.records.get((provider, model_id, field, protocol))
        if record is None:
            return result
        result.update(sources=record['sources'], investigated_at=record['investigated_at'])
        for source in record['sources']:
            url = source['url']
            if url not in self.cache:
                try:
                    self.cache[url] = hashlib.sha256(self.fetch(url, self.timeout)).hexdigest()
                except (OSError, URLError, TimeoutError, RuntimeError):
                    self.cache[url] = None
            if self.cache[url] != source['sha256']:
                result['conclusion'] = 'Source modifiée ou inaccessible : nouvelle investigation du LLM requise.'
                return result
        result.update(status=record['status'], conclusion=record['conclusion'])
        if record['status'] == 'verified':
            result['value'] = record['value']
        return result


def recheck_findings(findings, provider, model_id, protocol, timeout=15):
    """Recontrôler les preuves supplémentaires à la frontière de génération PLLM."""
    resolver = EvidenceResolver(timeout=timeout)
    for finding in findings:
        validate_record(finding)
        if (finding['provider'] != provider or finding['model_id'] != model_id
                or (finding['field'] == 'reasoning' and finding.get('protocol') != protocol)):
            raise RuntimeError('Preuve incompatible avec le fournisseur, modèle ou protocole')
        key = (provider, model_id, finding['field'], finding.get('protocol'))
        resolver.records[key] = finding
        checked = resolver.resolve(*key)
        if checked['status'] != 'verified':
            raise RuntimeError('Preuve supplémentaire non vérifiable : nouvelle investigation du LLM requise')
