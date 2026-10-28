#!/usr/bin/env python3
"""Mise à jour bornée des distributions Tools Codex ; bibliothèque standard."""

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import io
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid
import zipfile


REPOSITORY = 'AzenorPixs/tools-codex'
REPO_URL = 'https://github.com/' + REPOSITORY
MARKETPLACE = 'tools-codex'
LIMIT = 32 * 1024 * 1024
RECEIPT = '.tools-codex-origin.json'
PROMPT_COMMAND = '.codex/commands/PROMPT.md'
COMMAND_ALIASES = {name + '.md': name.lower() + '.md'
                   for name in ('CM', 'PLLM', 'TFL', 'TCU', 'LM', 'PROMPT')}
PROMPT_NAMES = ('PROMPT.md', 'prompt.md')
PROMPT_SKILL = 'skills/prompt/SKILL.md'
PROMPT_RESOLVER = 'skills/prompt/scripts/resolve_prompt.py'
PROMPT_RECEIPT = '.tools-codex-prompt-origin.json'
SUFFIXES = {'.py', '.md', '.json', '.yaml', '.yml', '.txt', '.svg', '.png', '.webp'}
EXCLUDED = {'data', '__pycache__', 'node_modules', '.git', 'logs', 'secrets.json',
            'secrets.yaml', 'credentials.json', 'credentials.yaml'}

_SCHEDULE_SPEC = importlib.util.spec_from_file_location('tcu_schedule', Path(__file__).with_name('scheduler.py'))
scheduler = importlib.util.module_from_spec(_SCHEDULE_SPEC)
_SCHEDULE_SPEC.loader.exec_module(scheduler)


class UpdateError(Exception):
    """Échec attendu, avec diagnostic sans contenu distant ni secret."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r'\d+\.\d+\.\d+(?:\+[\w.-]+)?', value):
        raise UpdateError('Version de release invalide')
    return tuple(map(int, value.split('+')[0].split('.')))


def safe_relative(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    if (not name or '\\' in name or any(ord(c) < 32 for c in name)
            or p.is_absolute() or '..' in p.parts or str(p) != name):
        raise UpdateError('Chemin relatif invalide')
    return p


def decode_json(raw: bytes | str) -> dict:
    def pairs(items):
        result = {}
        for key, val in items:
            if key in result:
                raise UpdateError('Clé JSON dupliquée')
            result[key] = val
        return result

    def invalid(_):
        raise UpdateError('Constante JSON non conforme')

    try:
        result = json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    except (ValueError, UnicodeError) as exc:
        raise UpdateError('Réponse JSON invalide') from exc
    if not isinstance(result, dict):
        raise UpdateError('Objet JSON attendu')
    return result


def allowed_url(url: str) -> bool:
    from urllib.parse import urlsplit
    try:
        p = urlsplit(url)
        return (p.scheme == 'https' and p.hostname in {'api.github.com', 'codeload.github.com'}
                and p.username is None and p.password is None and p.port in (None, 443))
    except ValueError:
        return False


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise UpdateError('Redirection GitHub non autorisée')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str) -> bytes:
    if not allowed_url(url):
        raise UpdateError('URL GitHub non autorisée')
    request = Request(url, headers={'Accept': 'application/vnd.github+json',
                                   'User-Agent': 'tools-codex-tcu'})
    try:
        with build_opener(SafeRedirect()).open(request, timeout=30) as response:
            data = response.read(LIMIT + 1)
    except HTTPError as exc:
        code = exc.code
        exc.close()
        raise UpdateError(f'GitHub : HTTP {code}') from exc
    except (URLError, TimeoutError) as exc:
        raise UpdateError('GitHub indisponible ou délai dépassé') from exc
    if len(data) > LIMIT:
        raise UpdateError('Réponse GitHub trop volumineuse')
    return data


def source_file(path: PurePosixPath) -> bool:
    return (not set(path.parts) & EXCLUDED and path.suffix in SUFFIXES
            and not any('.env' in part or part.startswith('.') for part in path.parts))


def snapshot(fetcher=fetch) -> dict:
    info = decode_json(fetcher('https://api.github.com/repos/' + REPOSITORY + '/commits/HEAD'))
    sha = info.get('sha')
    if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{40}', sha):
        raise UpdateError('SHA GitHub invalide')
    raw = fetcher('https://api.github.com/repos/' + REPOSITORY + '/zipball/' + sha)
    if len(raw) > LIMIT:
        raise UpdateError('Archive GitHub trop volumineuse')
    files = {}
    seen = set()
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if len(entries) > 5000 or sum(e.file_size for e in entries) > LIMIT * 2:
                raise UpdateError('Archive GitHub hors limites')
            roots = set()
            for entry in entries:
                if entry.is_dir():
                    continue
                full = safe_relative(entry.filename)
                if len(full.parts) < 2:
                    raise UpdateError('Racine d’archive invalide')
                roots.add(full.parts[0])
                name = str(PurePosixPath(*full.parts[1:]))
                if name in seen:
                    raise UpdateError('Fichier dupliqué dans l’archive')
                seen.add(name)
                p = PurePosixPath(name)
                selected = (name in {'VERSION', '.agents/plugins/marketplace.json'}
                            or re.fullmatch(r'plugins/[a-z0-9-]+/\.codex-plugin/plugin\.json', name)
                            or re.fullmatch(r'plugins/[a-z0-9-]+/hooks/hooks\.json', name)
                            or (len(p.parts) >= 3 and p.parts[0] == 'skills'
                                and re.fullmatch('[a-z0-9-]+', p.parts[1])
                                and source_file(PurePosixPath(*p.parts[2:])))
                            or (len(p.parts) == 3 and p.parts[:2] == ('.codex', 'commands')
                                and p.suffix == '.md'))
                if not selected:
                    continue
                mode = entry.external_attr >> 16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not stat.S_ISREG(mode)):
                    raise UpdateError('Source distante non régulière')
                if entry.file_size > 2 * 1024 * 1024:
                    raise UpdateError('Fichier source trop volumineux')
                files[name] = archive.read(entry)
            if len(roots) != 1:
                raise UpdateError('Plusieurs racines dans l’archive')
    except (zipfile.BadZipFile, RuntimeError, EOFError) as exc:
        raise UpdateError('Archive GitHub invalide') from exc
    try:
        release = files['VERSION'].decode('utf-8').strip()
        version(release)
        catalog = decode_json(files['.agents/plugins/marketplace.json'])
        plugins = catalog['plugins']
        if catalog['name'] != MARKETPLACE or not isinstance(plugins, list) or not plugins:
            raise UpdateError('Catalogue Tools Codex invalide')
        names = set()
        for plugin in plugins:
            name = plugin['name']
            if (not isinstance(name, str) or not re.fullmatch('[a-z0-9-]+', name)
                    or name in names or plugin['source'] != {'source': 'local', 'path': './plugins/' + name}):
                raise UpdateError('Entrée de marketplace invalide')
            names.add(name)
            manifest = decode_json(files[f'plugins/{name}/.codex-plugin/plugin.json'])
            if (manifest['name'] != name or version(manifest['version']) != version(release)
                    or manifest['skills'] != './skills/'):
                raise UpdateError('Releases des manifestes divergentes')
            if f'skills/{name}/SKILL.md' not in files:
                raise UpdateError('Skill du catalogue absent')
            if 'hooks' in manifest:
                if manifest['hooks'] != './hooks/hooks.json':
                    raise UpdateError('Chemin de hooks non pris en charge')
                hooks = decode_json(files[f'plugins/{name}/hooks/hooks.json'])
                expected = 'python3 "${PLUGIN_ROOT}/skills/' + name + '/scripts/scheduler.py" install --hook'
                expected_hooks = {'hooks': {'SessionStart': [{'hooks': [
                    {'type': 'command', 'command': expected, 'timeout': 60, 'async': True}]}]}}
                if (hooks != expected_hooks
                        or f'skills/{name}/scripts/scheduler.py' not in files):
                    raise UpdateError('Bootstrap de planning incomplet ou non conforme')
        if 'prompt' in names:
            if PROMPT_COMMAND not in files and '.codex/commands/prompt.md' in files:
                files[PROMPT_COMMAND] = files['.codex/commands/prompt.md']
            for resource in (PROMPT_COMMAND, PROMPT_SKILL, PROMPT_RESOLVER):
                if resource not in files or not files[resource].strip():
                    raise UpdateError('Composant prompt incomplet dans la source')
                files[resource].decode('utf-8')
        for name, data in files.items():
            if name.endswith('.py'):
                compile(data, name, 'exec')
            if name.startswith('skills/') and name.endswith('/SKILL.md'):
                text = data.decode('utf-8')
                if (not text.startswith('---\n') or '\n---\n' not in text[4:]
                        or not re.search(r'^name: '+re.escape(PurePosixPath(name).parts[1])+r'\s*$', text, re.M)
                        or not re.search(r'^description: .+', text, re.M)):
                    raise UpdateError('Skill distant invalide')
    except (KeyError, TypeError, UnicodeError, SyntaxError) as exc:
        raise UpdateError('Sources GitHub incomplètes ou invalides') from exc
    return {'sha': sha, 'version': release, 'files': files, 'plugins': names}


def codex(args: list[str]) -> dict:
    try:
        result = subprocess.run(['codex', 'plugin', *args], capture_output=True,
                                text=True, timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise UpdateError('CLI Codex indisponible ou délai dépassé') from exc
    if result.returncode:
        raise UpdateError(f'CLI Codex : échec de {args[0]} (code {result.returncode})')
    return decode_json(result.stdout)


def installed(runner=codex) -> dict:
    result = runner(['list', '--marketplace', MARKETPLACE, '--json'])
    entries = result.get('installed')
    if not isinstance(entries, list):
        raise UpdateError('Liste des plugins installés invalide')
    plugins = {}
    for entry in entries:
        try:
            name = entry['name']
            origin = entry['marketplaceSource']
            if (not isinstance(name, str) or not re.fullmatch('[a-z0-9-]+', name)
                    or name in plugins or entry['marketplaceName'] != MARKETPLACE
                    or entry['pluginId'] != name + '@' + MARKETPLACE
                    or entry['installed'] is not True or not isinstance(entry['enabled'], bool)
                    or origin['sourceType'] != 'git'
                    or origin['source'] not in {REPO_URL, REPO_URL + '.git'}):
                raise UpdateError('Origine ou identité de plugin ambiguë')
            version(entry['version'])
        except (KeyError, TypeError) as exc:
            raise UpdateError('Métadonnées de plugin incomplètes') from exc
        plugins[name] = entry
    return plugins


def no_links(path: Path) -> None:
    for p in (path, *path.parents):
        if p.is_symlink():
            raise UpdateError('Lien local préservé sans modification')


def development(path: Path) -> bool:
    return any((p / '.git').exists() or
               ((p / 'VERSION').is_file() and (p / '.agents/plugins/marketplace.json').is_file())
               for p in (path, *path.parents))


def prepare_local(item: dict, target: Path, selected: dict, remote: dict,
                  adopt: bool, receipt_name=RECEIPT, allow_create=False,
                  ignore_names=frozenset(), inherit_name=None) -> dict:
    try:
        no_links(target)
        if development(target):
            raise UpdateError('Checkout de développement préservé')
        if target.exists() and not target.is_dir():
            raise UpdateError('Répertoire de distribution attendu')
        if not target.exists() and not allow_create:
            return item
        receipt_path = target / receipt_name
        no_links(receipt_path)
        receipt = None
        if receipt_path.exists():
            receipt = decode_json(receipt_path.read_bytes())
        elif inherit_name is not None:
            legacy_path = target / inherit_name
            no_links(legacy_path)
            if legacy_path.is_file():
                legacy = decode_json(legacy_path.read_bytes())
                if isinstance(legacy.get('hashes'), dict) and any(n in legacy['hashes'] for n in selected):
                    receipt = {**legacy, 'hashes': {n: legacy['hashes'][n] for n in selected if n in legacy['hashes']}}
        if receipt is not None:
            if (receipt.get('repository') != REPOSITORY or receipt.get('schema') != 1
                    or not isinstance(receipt.get('hashes'), dict)
                    or not re.fullmatch('[0-9a-f]{40}', receipt.get('sha', ''))):
                raise UpdateError('Reçu de provenance invalide')
            receipt['hashes'] = {n: h for n, h in receipt['hashes'].items() if n not in ignore_names}
            item['avant'] = receipt['version']
            if version(receipt['version']) > version(remote['version']):
                raise UpdateError('Retour de version refusé')
            for rel, old_hash in receipt['hashes'].items():
                safe_relative(rel)
                if not source_file(PurePosixPath(rel)):
                    raise UpdateError('Source suivie invalide')
                path = target / rel
                no_links(path)
                if not path.is_file() or digest(path.read_bytes()) != old_hash:
                    raise UpdateError('Modification locale d’un fichier suivi')
        originals = {}
        for rel, data in selected.items():
            safe_relative(rel)
            path = target / rel
            no_links(path)
            if path.exists() and not path.is_file():
                raise UpdateError('Cible source non régulière')
            current = path.read_bytes() if path.exists() else None
            originals[rel] = current
            tracked = receipt and rel in receipt['hashes']
            if current is not None and current != data and not tracked and not adopt:
                raise UpdateError('Copie sans provenance : adoption explicite nécessaire')
        if not receipt and not adopt and not allow_create and any(v is None for v in originals.values()):
            raise UpdateError('Installation incomplète sans provenance')
        same = all(originals[n] == b for n, b in selected.items())
        if same and receipt is None:
            item['avant'] = remote['version']
        item.update(status='courant' if same else 'pret', apres=item['avant'], target=target,
                    selected=selected, originals=originals, receipt=receipt, receipt_name=receipt_name,
                    receipt_bytes=receipt_path.read_bytes() if receipt_path.exists() else None)
    except (UpdateError, OSError, KeyError, TypeError) as exc:
        item.update(status='conflit', cause=str(exc) if isinstance(exc, UpdateError) else 'Provenance ou accès local invalide')
    return item


def command_names(name: str) -> tuple[str, ...]:
    canonical = name[:-3].upper() + '.md'
    if canonical in COMMAND_ALIASES:
        return canonical, COMMAND_ALIASES[canonical]
    return (name,)


def local_plan(remote: dict, roots: list[tuple[str, Path]], adopt: bool) -> list[dict]:
    plans = []
    seen = set()
    files = remote['files']
    skills = sorted({PurePosixPath(n).parts[1] for n in files if n.startswith('skills/')})
    for kind, root in roots:
        for name in skills if kind == 'skills' else ['commands']:
            target = root / name if kind == 'skills' else root
            key = str(target.absolute())
            if key in seen:
                continue
            seen.add(key)
            item = {'brique': str(target), 'canal': 'github', 'avant': None,
                    'apres': None, 'cible': remote['version'], 'status': 'absent'}
            plans.append(item)
            if not target.exists() and not target.is_symlink():
                continue
            if kind == 'skills':
                prefix = f'skills/{name}/'
                selected = {n[len(prefix):]: b for n, b in files.items() if n.startswith(prefix)}
                if not (target / 'SKILL.md').is_file() and not target.is_symlink():
                    item.update(status='conflit', cause='Origine du skill ambiguë')
                    continue
            else:
                commands = {PurePosixPath(n).name: b for n, b in files.items()
                            if n.startswith('.codex/commands/')}
                selected = {}
                for name, data in commands.items():
                    if name in PROMPT_NAMES and 'prompt' in remote['plugins']:
                        continue
                    variants = command_names(name)
                    data = commands.get(variants[0], data)
                    for rel in variants:
                        if (target / rel).exists() or (target / rel).is_symlink():
                            selected[rel] = data
                if not selected:
                    continue
            prepare_local(item, target, selected, remote, adopt,
                          ignore_names=set(PROMPT_NAMES) if kind == 'commands' and 'prompt' in remote['plugins'] else frozenset())
    return plans


def prompt_command_plans(home: Path, roots: list, remote: dict, adopt: bool) -> list[dict]:
    if 'prompt' not in remote['plugins']:
        return []
    folders = [root for kind, root in roots if kind == 'commands'] or [home / 'prompts']
    plans = []
    seen = set()
    for i, root in enumerate(folders):
        names = [name for name in PROMPT_NAMES
                 if (root / name).exists() or (root / name).is_symlink()]
        key = str(root.absolute())
        if key in seen or (i > 0 and not names):
            continue
        seen.add(key)
        if not names:
            names = [PROMPT_NAMES[0]]
        path = root / names[0]
        item = {'brique': str(path), 'canal': 'github', 'composant': 'prompt', 'ressource': 'commande',
                'avant': None, 'apres': None, 'cible': remote['version'], 'status': 'absent',
                'operation': 'mettre_a_jour' if path.exists() or path.is_symlink() else 'installer'}
        plans.append(prepare_local(item, root, {name: remote['files'][PROMPT_COMMAND] for name in names},
                                   remote, adopt, PROMPT_RECEIPT, allow_create=True, inherit_name=RECEIPT))
    return plans


def atomic_write(path: Path, data: bytes) -> None:
    no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.tcu-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def apply_local(plans: list[dict], remote: dict, backup: Path, writer=atomic_write) -> None:
    changes = []
    for i, item in enumerate(plans):
        if item['status'] not in {'pret', 'courant'}:
            continue
        target = item['target']
        old_hashes = dict(item['receipt']['hashes']) if item['receipt'] else {}
        for rel, data in item['selected'].items():
            old_hashes[rel] = digest(data)
            p = target / rel
            no_links(p)
            current = p.read_bytes() if p.exists() else None
            if current != item['originals'][rel]:
                raise UpdateError('Modification concurrente avant application')
            if current != data:
                changes.append((p, data, current, f'{i}/{rel}'))
        old_receipt = item['receipt_bytes']
        receipt_name = item.get('receipt_name', RECEIPT)
        receipt_path = target / receipt_name
        no_links(receipt_path)
        current = receipt_path.read_bytes() if receipt_path.exists() else None
        if current != old_receipt:
            raise UpdateError('Reçu modifié pendant la préparation')
        receipt = {'schema': 1, 'repository': REPOSITORY, 'sha': remote['sha'],
                   'version': remote['version'], 'hashes': old_hashes}
        changes.append((receipt_path, (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode(),
                        old_receipt, f'{i}/{receipt_name}'))
    for _, _, original, rel in changes:
        if original is not None:
            atomic_write(backup / 'sources' / rel, original)
    journal = []
    try:
        for path, data, original, _ in changes:
            no_links(path)
            if (path.read_bytes() if path.exists() else None) != original:
                raise UpdateError('Modification concurrente pendant application')
            journal.append((path, original))
            writer(path, data)
    except BaseException as original_error:
        # Nettoyage transactionnel, puis propagation sans masquer la cause.
        failures = []
        for path, original in reversed(journal):
            try:
                no_links(path)
                if original is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic_write(path, original)
            except (OSError, UpdateError) as exc:
                failures.append(exc)
        if failures:
            raise UpdateError('Restauration autonome incomplète ; sauvegarde conservée') from original_error
        raise
    for item in plans:
        if item['status'] in {'pret', 'courant'}:
            item['status'] = 'mis_a_jour' if item['status'] == 'pret' else 'courant'
            item['apres'] = remote['version']


def cache_root(home: Path, name: str, release: str) -> Path:
    return home / 'plugins/cache' / MARKETPLACE / name / release


def save_data(home: Path, plugins: dict, backup: Path) -> list[tuple[str, str, bytes]]:
    saved = []
    for name, entry in plugins.items():
        package = cache_root(home, name, entry['version'])
        no_links(package)
        manifest = package / '.codex-plugin/plugin.json'
        no_links(manifest)
        if not manifest.is_file():
            raise UpdateError('Cache installé introuvable : données non garanties')
        metadata = decode_json(manifest.read_bytes())
        if metadata.get('name') != name or metadata.get('version') != entry['version']:
            raise UpdateError('Identité du cache installé invalide')
        data_root = package / 'skills' / name / 'data'
        no_links(data_root)
        if not data_root.exists():
            continue
        for p in sorted(data_root.rglob('*')):
            no_links(p)
            if p.is_dir():
                continue
            rel = str(p.relative_to(data_root))
            if not p.is_file() or p.suffix not in {'.json', '.md'} or not source_file(PurePosixPath(rel)):
                raise UpdateError('Données non prises en charge : rafraîchissement suspendu')
            content = p.read_bytes()
            atomic_write(backup / 'plugin-data' / name / rel, content)
            saved.append((name, rel, content))
    return saved


def restore_data(home: Path, plugins: dict, saved: list) -> None:
    for name, rel, data in saved:
        if name not in plugins:
            raise UpdateError('Plugin absent après mise à jour ; sauvegarde conservée')
        package = cache_root(home, name, plugins[name]['version'])
        metadata_path = package / '.codex-plugin/plugin.json'
        no_links(metadata_path)
        metadata = decode_json(metadata_path.read_bytes())
        if metadata.get('version') != plugins[name]['version'] or metadata.get('name') != name:
            raise UpdateError('Cache après mise à jour non vérifiable')
        atomic_write(package / 'skills' / name / 'data' / rel, data)


@contextmanager
def application_lock(home: Path):
    no_links(home)
    home.mkdir(parents=True, exist_ok=True)
    path = home / 'tcu.lock'
    no_links(path)
    with path.open('a+b') as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise UpdateError('Une application TCU est déjà en cours') from exc
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def prompt_skill_state(home: Path, entry: dict | None, remote: dict, strict=False) -> tuple:
    if entry is None:
        return None, None
    try:
        root = cache_root(home, 'prompt', entry['version'])
        manifest_path = root / '.codex-plugin/plugin.json'
        no_links(manifest_path)
        metadata = decode_json(manifest_path.read_bytes())
        if (metadata.get('name') != 'prompt' or metadata.get('version') != entry['version']
                or metadata.get('skills') != './skills/'):
            raise UpdateError('Manifeste installé du composant prompt invalide')
        for source in (PROMPT_SKILL, PROMPT_RESOLVER):
            path = root / source
            no_links(path)
            if not path.is_file():
                raise UpdateError('Skill embarqué ou résolveur prompt absent')
            if strict and path.read_bytes() != remote['files'][source]:
                raise UpdateError('Sources du skill prompt installé divergentes')
        return entry['version'], None
    except (UpdateError, OSError) as exc:
        return None, str(exc) if isinstance(exc, UpdateError) else 'Cache du skill prompt non vérifiable'


def execute(home: Path, roots: list, apply=False, adopt=False, fetcher=fetch, runner=codex) -> dict:
    remote = snapshot(fetcher)
    before = installed(runner)
    if any(n not in remote['plugins'] for n in before):
        raise UpdateError('Plugin installé absent du catalogue officiel')
    if any(version(e['version']) > version(remote['version']) for e in before.values()):
        raise UpdateError('Retour de version marketplace refusé')
    managed = {'prompt'} & remote['plugins']
    plans = local_plan(remote, roots, adopt) + prompt_command_plans(home, roots, remote, adopt)
    report = {'release_github': remote['version'], 'sha': remote['sha'], 'mode': 'apply' if apply else 'check',
              'succes': False, 'briques': [], 'backup': None}
    for name in sorted(remote['plugins']):
        entry = before.get(name)
        report['briques'].append({'brique': name, 'canal': 'marketplace', 'ressource': 'plugin',
                                  'avant': entry['version'] if entry else None,
                                  'apres': entry['version'] if entry else None,
                                  'cible': remote['version'],
                                  'status': ('a_verifier' if not apply else 'en_attente') if entry
                                  else 'a_installer' if name in managed else 'absent'})
    skill_row = None
    if managed:
        actual, cause = prompt_skill_state(home, before.get('prompt'), remote)
        skill_row = {'brique': 'prompt/skill', 'composant': 'prompt', 'ressource': 'skill',
                     'canal': 'marketplace', 'avant': actual, 'apres': actual,
                     'cible': remote['version'],
                     'status': 'a_verifier' if actual else 'a_reparer' if 'prompt' in before else 'a_installer'}
        if cause:
            skill_row['cause'] = cause
        report['briques'].append(skill_row)
    public_keys = {'brique', 'canal', 'avant', 'apres', 'cible', 'status', 'cause',
                   'composant', 'ressource', 'operation'}

    def register_schedule():
        if any(item['status'] == 'conflit' and Path(item['brique']).name in {'tfl', 'pllm'}
               for item in plans):
            report['briques'].append({'brique': 'llm-refresh', 'canal': 'session_utilisateur',
                                      'ressource': 'planification', 'avant': None, 'apres': None,
                                      'cible': None, 'status': 'conflit',
                                      'cause': 'Source TFL ou PLLM en conflit ; planning inchangé'})
            return
        def schedule_runner(arguments, **kwargs):
            if arguments[1:3] == ['plugin', 'list']:
                return subprocess.CompletedProcess(arguments, 0, json.dumps(runner(arguments[2:])))
            return scheduler.command(arguments, **kwargs)
        try:
            state = scheduler.install(home, [p for kind, p in roots if kind == 'skills'],
                                      apply=apply, runner=schedule_runner)
        except (scheduler.ScheduleError, OSError) as error:
            state = {'status': 'incomplet', 'cause': str(error) if isinstance(error, scheduler.ScheduleError)
                     else 'Installation du planning impossible'}
            report['erreur'] = 'Planning utilisateur non installé ou non vérifiable'
        report['briques'].append({'brique': 'llm-refresh', 'canal': 'session_utilisateur',
                                  'ressource': 'planification', 'avant': None, 'apres': None,
                                  'cible': None, **state})

    def mark_unapplied():
        for item in plans:
            if item['status'] == 'pret':
                item['status'] = 'non_applique'

    def finish():
        report['briques'].extend({k: v for k, v in item.items() if k in public_keys} for item in plans)
        report['succes'] = not report.get('erreur') and not any(
            row['status'] in {'conflit', 'inconnu', 'incomplet', 'non_applique'} for row in report['briques'])
        for row in report['briques']:
            if (row.get('composant') == 'prompt' or row['brique'] in {'prompt', 'prompt/skill'}
                    or Path(row['brique']).name in {'prompt', *PROMPT_NAMES}):
                row['libelle'] = 'PROMPT'
        report['nouvelle_session'] = 'Ouvrir une nouvelle session Codex pour charger les skills actualisés.'
        return report

    def observe(state):
        plugin_rows = {r['brique']: r for r in report['briques'] if r.get('ressource') == 'plugin'}
        for name in state.keys() - plugin_rows.keys():
            row = {'brique': name, 'canal': 'marketplace', 'ressource': 'plugin', 'avant': None}
            report['briques'].append(row)
            plugin_rows[name] = row
        for name, row in plugin_rows.items():
            entry = state.get(name)
            row['apres'] = entry['version'] if entry else None
            row['status'] = ('installe' if row['avant'] is None else
                             'mis_a_jour' if row['avant'] != row['apres'] else 'courant') if entry else 'absent'
        if skill_row is not None:
            actual, cause = prompt_skill_state(home, state.get('prompt'), remote, strict=True)
            skill_row['apres'] = actual
            if cause:
                skill_row.update(status='incomplet', cause=cause)
            else:
                skill_row.pop('cause', None)
                skill_row['status'] = ('installe' if skill_row['avant'] is None else
                                       'mis_a_jour' if actual != skill_row['avant'] else 'courant') if actual else 'absent'

    def verify(state, require_prompt=False):
        if (not set(before).issubset(state) or set(state) - set(before) - managed
                or any(state[n]['enabled'] != before[n]['enabled'] for n in before)
                or any(version(e['version']) != version(remote['version']) for e in state.values())):
            raise UpdateError('État marketplace divergent : sources autonomes non appliquées')
        if require_prompt and managed:
            if 'prompt' not in state or ('prompt' not in before and not state['prompt']['enabled']):
                raise UpdateError('Installation ou activation de prompt non vérifiée')
            if skill_row['apres'] is None:
                raise UpdateError('Composant prompt installé incomplet ; wrapper non appliqué')

    if not apply:
        register_schedule()
        return finish()
    with application_lock(home):
        backup = home / 'tcu-backups' / uuid.uuid4().hex
        no_links(backup)
        backup.mkdir(parents=True, mode=0o700)
        backup.chmod(0o700)
        report['backup'] = str(backup)
        try:
            saved = save_data(home, before, backup)
        except (UpdateError, OSError) as exc:
            report['erreur'] = str(exc) if isinstance(exc, UpdateError) else 'Sauvegarde des données impossible'
            mark_unapplied()
            return finish()

        def inspect_after():
            try:
                state = installed(runner)
            except UpdateError:
                report['erreur'] = 'État marketplace après opération non vérifiable ; sauvegarde conservée'
                for row in report['briques']:
                    if row['canal'] == 'marketplace' and (row['avant'] is not None or row['brique'] in managed):
                        row.update(status='inconnu', apres=None)
                if skill_row is not None:
                    skill_row.update(status='inconnu', apres=None)
                return None
            observe(state)
            try:
                restore_data(home, state, saved)
            except (UpdateError, OSError) as exc:
                report['erreur'] = str(exc) if isinstance(exc, UpdateError) else 'Restitution des données impossible ; sauvegarde conservée'
                return None
            return state

        failure = None
        try:
            runner(['marketplace', 'upgrade', MARKETPLACE, '--json'])
        except UpdateError as exc:
            failure = str(exc)
        after = inspect_after()
        if after is None:
            mark_unapplied()
            return finish()
        try:
            if failure:
                raise UpdateError(failure)
            verify(after)
            if managed and ('prompt' not in after or skill_row['apres'] is None):
                try:
                    runner(['add', 'prompt@' + MARKETPLACE, '--json'])
                except UpdateError as exc:
                    failure = str(exc)
                after = inspect_after()
                if after is None:
                    mark_unapplied()
                    return finish()
                if failure:
                    raise UpdateError(failure)
            verify(after, require_prompt=True)
            apply_local(plans, remote, backup)
            register_schedule()
        except (UpdateError, OSError) as exc:
            report['erreur'] = str(exc) if isinstance(exc, UpdateError) else 'Écriture impossible ; sauvegarde conservée'
            mark_unapplied()
        return finish()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', nargs='?', choices=('check',), help='Contrôle sans écriture')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Contrôle sans écriture (défaut)')
    mode.add_argument('--apply', action='store_true', help='Appliquer les mises à jour')
    parser.add_argument('--adopt', action='store_true', help='Adopter explicitement les copies historiques sans reçu, avec sauvegarde')
    parser.add_argument('--skills-dir', action='append', type=Path, help='Racine de skills autonomes existants (répétable)')
    parser.add_argument('--commands-dir', action='append', type=Path, help='Répertoire de commandes existantes (répétable)')
    args = parser.parse_args(argv)
    if args.action == 'check' and args.apply:
        parser.error('check ne peut pas être combiné à --apply')
    home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).absolute()
    roots = [('skills', p.expanduser().absolute()) for p in
             (args.skills_dir or [home / 'skills', Path.home() / '.agents/skills'])]
    roots.extend(('commands', p.expanduser().absolute()) for p in
                 (args.commands_dir or [home / 'prompts', home / 'commands']))
    try:
        result = execute(home, roots, args.apply, args.adopt)
    except (UpdateError, OSError) as exc:
        result = {'succes': False, 'erreur': str(exc) if isinstance(exc, UpdateError) else 'Accès local ou réseau impossible'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['succes'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
