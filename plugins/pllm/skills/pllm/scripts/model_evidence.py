"""Conclusions d'investigation du LLM, vérifiées sans inférence de modèle ou de route."""

from datetime import datetime
import hashlib
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import unicodedata
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

PROVIDERS = ('opencode_go', 'opencode', 'openrouter', 'deepseek')
PROTOCOLS = ('chat_completions', 'responses', 'messages')
MAX_BYTES = 2_000_000
HTML_FINGERPRINT = 'html_visible_text_v1'
RAW_FINGERPRINT = 'raw_bytes_v1'


class _VisibleText(HTMLParser):
    """Extract visible HTML text without volatile markup or embedded scripts."""

    _SKIP_TAGS = {'head', 'script', 'style', 'noscript', 'template', 'svg', 'nav', 'header', 'footer'}
    _BLOCK_TAGS = {'address', 'article', 'aside', 'blockquote', 'br', 'dd', 'div', 'dl', 'dt', 'h1', 'h2',
                   'h3', 'h4', 'h5', 'h6', 'li', 'main', 'ol', 'p', 'section', 'table', 'td', 'th', 'tr', 'ul'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._skip_tag = None
        self._parts = []

    def handle_starttag(self, tag, attrs):
        if self._skip_tag is None and tag in self._SKIP_TAGS:
            self._skip_tag = tag
        elif self._skip_tag is None and tag in self._BLOCK_TAGS:
            self._parts.append(' ')

    def handle_endtag(self, tag):
        if self._skip_tag == tag:
            self._skip_tag = None
        elif self._skip_tag is None and tag in self._BLOCK_TAGS:
            self._parts.append(' ')

    def handle_data(self, data):
        if self._skip_tag is None:
            self._parts.append(data)

    def visible_text(self):
        return unicodedata.normalize('NFC', ' '.join(' '.join(self._parts).split()))


def source_fingerprint(raw, method=None):
    """Return a stable SHA-256 for visible HTML text or exact non-HTML bytes."""
    prefix = raw.lstrip()[:4096].lower()
    detected = (HTML_FINGERPRINT if b'<html' in prefix or b'<!doctype html' in prefix
                else RAW_FINGERPRINT)
    method = detected if method is None else method
    if method == HTML_FINGERPRINT:
        if detected != HTML_FINGERPRINT:
            raise RuntimeError('Preuve : empreinte HTML attendue')
        parser = _VisibleText()
        try:
            parser.feed(raw.decode('utf-8'))
        except UnicodeError as error:
            raise RuntimeError('Preuve : source HTML non UTF-8') from error
        payload = parser.visible_text().encode('utf-8')
        if not payload:
            raise RuntimeError('Preuve : source HTML sans texte visible')
    elif method == RAW_FINGERPRINT:
        payload = raw
    else:
        raise RuntimeError('Preuve : méthode d’empreinte inconnue')
    return method, hashlib.sha256(payload).hexdigest()


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
    original = urlsplit(source_url(url))
    request = Request(url, headers={'Accept': 'text/html,text/markdown,application/json',
                                    'User-Agent': 'TFL/1.0'})
    with urlopen(request, timeout=timeout) as response:
        redirected = urlsplit(response.geturl())
        if (redirected.scheme != 'https' or redirected.hostname != original.hostname
                or redirected.username is not None or redirected.password is not None
                or redirected.fragment or redirected.port not in (None, 443)):
            raise RuntimeError('Preuve : redirection de source hors origine interdite')
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
                    or source.get('fingerprint_method', RAW_FINGERPRINT) not in (RAW_FINGERPRINT, HTML_FINGERPRINT)
                    or datetime.fromisoformat(source['retrieved_at']).tzinfo is None):
                raise ValueError('source')
        if record['status'] == 'verified':
            value = record['value']
            if record['field'] == 'context':
                if type(value) is not int or value <= 0:
                    raise ValueError('contexte')
            else:
                levels = value['supported_efforts']
                if ((levels is not None and (not isinstance(levels, list) or not levels
                                             or any(not isinstance(level, str) for level in levels)))
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
                    method = source.get('fingerprint_method', RAW_FINGERPRINT)
                    _, self.cache[url] = source_fingerprint(self.fetch(url, self.timeout), method)
                except (OSError, URLError, TimeoutError, RuntimeError):
                    self.cache[url] = None
            if self.cache[url] != source['sha256']:
                result['conclusion'] = 'Source modifiée ou inaccessible : nouvelle investigation du LLM requise.'
                return result
        if (record['status'] == 'verified' and field == 'reasoning'
                and record['value']['supported_efforts'] is not None
                and 'medium' not in record['value']['supported_efforts']):
            result['conclusion'] = 'La preuve historique ne couvre pas Medium ; une nouvelle preuve est requise.'
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
        if checked['status'] == 'unsupported':
            raise RuntimeError(checked['conclusion'])
        if checked['status'] != 'verified':
            raise RuntimeError('Preuve supplémentaire non vérifiable : '
                               + checked.get('conclusion', 'nouvelle investigation requise'))
