#!/usr/bin/env python3
"""Mise à jour bornée des distributions Tools Codex ; bibliothèque standard."""

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import io
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
SUFFIXES = {'.py', '.md', '.json', '.yaml', '.yml', '.txt', '.svg', '.png', '.webp'}
EXCLUDED = {'data', '__pycache__', 'node_modules', '.git', 'logs', 'secrets.json',
            'secrets.yaml', 'credentials.json', 'credentials.yaml'}


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


def local_plan(remote: dict, roots: list[tuple[str, Path]], adopt: bool) -> list[dict]:
    plans = []
    seen = set()
    files = remote['files']
    skills = sorted({PurePosixPath(n).parts[1] for n in files if n.startswith('skills/')})
    for kind, root in roots:
        candidates = skills if kind == 'skills' else ['commands']
        for name in candidates:
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
            try:
                no_links(target)
                if development(target):
                    raise UpdateError('Checkout de développement préservé')
                if not target.is_dir():
                    raise UpdateError('Répertoire de distribution attendu')
                if kind == 'skills':
                    if not (target / 'SKILL.md').is_file():
                        raise UpdateError('Origine du skill ambiguë')
                    prefix = f'skills/{name}/'
                    selected = {n[len(prefix):]: b for n, b in files.items() if n.startswith(prefix)}
                else:
                    selected = {PurePosixPath(n).name: b for n, b in files.items()
                                if n.startswith('.codex/commands/') and (target / PurePosixPath(n).name).exists()}
                    if not selected:
                        continue
                receipt_path = target / RECEIPT
                no_links(receipt_path)
                receipt = None
                if receipt_path.exists():
                    receipt = decode_json(receipt_path.read_bytes())
                    if (receipt.get('repository') != REPOSITORY or receipt.get('schema') != 1
                            or not isinstance(receipt.get('hashes'), dict)
                            or not re.fullmatch('[0-9a-f]{40}', receipt.get('sha', ''))):
                        raise UpdateError('Reçu de provenance invalide')
                    item['avant'] = receipt['version']
                    if version(receipt['version']) > version(remote['version']):
                        raise UpdateError('Retour de version refusé')
                    for rel, old_hash in receipt['hashes'].items():
                        safe_relative(rel)
                        if not source_file(PurePosixPath(rel)):
                            raise UpdateError('Source suivie invalide')
                        p = target / rel
                        no_links(p)
                        if not p.is_file() or digest(p.read_bytes()) != old_hash:
                            raise UpdateError('Modification locale d’un fichier suivi')
                originals = {}
                for rel, data in selected.items():
                    safe_relative(rel)
                    p = target / rel
                    no_links(p)
                    if p.exists() and not p.is_file():
                        raise UpdateError('Cible source non régulière')
                    current = p.read_bytes() if p.exists() else None
                    originals[rel] = current
                    tracked = receipt and rel in receipt['hashes']
                    if current is not None and current != data and not tracked and not adopt:
                        raise UpdateError('Copie sans provenance : adoption explicite nécessaire')
                if not receipt and not adopt and any(v is None for v in originals.values()):
                    raise UpdateError('Installation incomplète sans provenance')
                same = all(originals[n] == b for n, b in selected.items())
                if same and receipt is None:
                    item['avant'] = remote['version']
                item.update(status='courant' if same else 'pret', apres=item['avant'],
                            target=target, selected=selected, originals=originals,
                            receipt=receipt, receipt_bytes=receipt_path.read_bytes() if receipt else None)
            except (UpdateError, OSError, KeyError, TypeError) as exc:
                item.update(status='conflit', cause=str(exc) if isinstance(exc, UpdateError) else 'Provenance ou accès local invalide')
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
        receipt_path = target / RECEIPT
        no_links(receipt_path)
        current = receipt_path.read_bytes() if receipt_path.exists() else None
        if current != old_receipt:
            raise UpdateError('Reçu modifié pendant la préparation')
        receipt = {'schema': 1, 'repository': REPOSITORY, 'sha': remote['sha'],
                   'version': remote['version'], 'hashes': old_hashes}
        changes.append((receipt_path, (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode(),
                        old_receipt, f'{i}/{RECEIPT}'))
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


def execute(home: Path, roots: list, apply=False, adopt=False, fetcher=fetch, runner=codex) -> dict:
    remote = snapshot(fetcher)
    before = installed(runner)
    if any(n not in remote['plugins'] for n in before):
        raise UpdateError('Plugin installé absent du catalogue officiel')
    if any(version(e['version']) > version(remote['version']) for e in before.values()):
        raise UpdateError('Retour de version marketplace refusé')
    plans = local_plan(remote, roots, adopt)
    report = {'release_github': remote['version'], 'sha': remote['sha'], 'mode': 'apply' if apply else 'check',
              'succes': False, 'briques': [], 'backup': None}
    for name, entry in before.items():
        report['briques'].append({'brique': name, 'canal': 'marketplace', 'avant': entry['version'],
                                  'apres': entry['version'], 'status': 'a_verifier' if not apply else 'en_attente'})
    for name in sorted(remote['plugins'] - before.keys()):
        report['briques'].append({'brique': name, 'canal': 'marketplace', 'avant': None,
                                  'apres': None, 'status': 'absent'})
    public_keys = {'brique', 'canal', 'avant', 'apres', 'cible', 'status', 'cause'}

    def finish():
        report['briques'].extend({k: v for k, v in p.items() if k in public_keys} for p in plans)
        report['succes'] = not report.get('erreur') and not any(p['status'] == 'conflit' for p in plans)
        report['nouvelle_session'] = 'Ouvrir une nouvelle session Codex pour charger les skills actualisés.'
        return report

    if not apply:
        return finish()
    if any(p['status'] == 'conflit' for p in plans):
        report['erreur'] = 'Conflits locaux : aucune application lancée'
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
            for item in plans:
                if item['status'] == 'pret':
                    item['status'] = 'non_applique'
            return finish()
        after = before
        failure = None
        try:
            runner(['marketplace', 'upgrade', MARKETPLACE, '--json'])
        except UpdateError as exc:
            failure = str(exc)
        try:
            after = installed(runner)
        except UpdateError:
            report['erreur'] = 'État marketplace après opération non vérifiable ; sauvegarde conservée'
            for row in report['briques']:
                if row['canal'] == 'marketplace' and row['avant'] is not None:
                    row.update(status='inconnu', apres=None)
            for item in plans:
                if item['status'] == 'pret':
                    item['status'] = 'non_applique'
            return finish()
        for row in report['briques']:
            entry = after.get(row['brique'])
            row.update(apres=entry['version'] if entry else None,
                       status=('mis_a_jour' if entry and entry['version'] != row['avant']
                               else 'courant' if entry else 'absent'))
        for name in sorted(after.keys() - remote['plugins']):
            report['briques'].append({'brique': name, 'canal': 'marketplace', 'avant': None,
                                      'apres': after[name]['version'], 'status': 'inattendu'})
        try:
            restore_data(home, after, saved)
            if failure:
                raise UpdateError(failure)
            if (set(after) != set(before) or any(after[n]['enabled'] != before[n]['enabled'] for n in before)
                    or any(version(e['version']) != version(remote['version']) for e in after.values())):
                raise UpdateError('État marketplace divergent : sources autonomes non appliquées')
            apply_local(plans, remote, backup)
        except (UpdateError, OSError) as exc:
            report['erreur'] = str(exc) if isinstance(exc, UpdateError) else 'Écriture impossible ; sauvegarde conservée'
            for item in plans:
                if item['status'] == 'pret':
                    item['status'] = 'non_applique'
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
