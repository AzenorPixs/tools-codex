#!/usr/bin/env python3
"""Planning utilisateur TFL puis PLLM ; aucune opération à l'import."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import shutil
import stat
import subprocess
import sys
import tempfile
import time


UNIT = 'tools-codex-llm-refresh'
CALENDAR = '*-*-* 00,12:00:00 Europe/Paris'
MARKER = '# Tools Codex managed llm refresh\n'
LIMIT = 1024 * 1024
SCRIPT_TIMEOUT = 3600
FILES = {'tfl': 'test_fournisseur_llm.py', 'pllm': 'evaluate.py'}


class ScheduleError(RuntimeError):
    """Diagnostic fixe, sans réponse distante ni configuration privée."""


def command(args, timeout=20, **kwargs):
    try:
        return subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, timeout=timeout, **kwargs)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ScheduleError('Commande locale indisponible ou délai dépassé') from error


def home_path():
    return Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).absolute()


def config_path():
    return Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))).absolute()


def safe(path):
    path = Path(path).absolute()
    if any(c in str(path) for c in ('\n', '\r', '\x00')):
        raise ScheduleError('Chemin non conforme')
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ScheduleError('Lien refusé dans un chemin géré')
    if path.exists() and path.stat().st_uid != os.getuid():
        raise ScheduleError('Fichier géré appartenant à un autre utilisateur')
    return path


def atomic_write(path, content):
    path = safe(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.llm-refresh-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def read_json(path):
    path = safe(path)
    if path.stat().st_size > LIMIT:
        raise ScheduleError('Métadonnées trop volumineuses')
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise ScheduleError('Métadonnées du planning invalides') from error
    if not isinstance(value, dict):
        raise ScheduleError('Métadonnées du planning invalides')
    return value


def development(path):
    return any((p / 'VERSION').is_file() and (p / '.agents/plugins/marketplace.json').is_file()
               for p in (path, *path.parents))


def package(path, name):
    try:
        path = safe(path)
        if development(path):
            return None
        for filename in (FILES[name], 'performance.py', 'model_blacklist.py'):
            target = safe(path / 'scripts' / filename)
            if not target.is_file():
                return None
        return path
    except (OSError, ScheduleError):
        return None


def discover(home, roots=(), runner=command, codex=None):
    roots = list(dict.fromkeys([Path(p).absolute() for p in roots] +
                              [home / 'skills', home.parent / '.agents/skills']))
    found = {}
    for name in FILES:
        for root in roots:
            candidate = package(root / name, name)
            if candidate is not None:
                found[name] = candidate
                break
    if len(found) == 2:
        return found
    executable = codex or shutil.which('codex')
    if not executable:
        return found
    result = runner([str(executable), 'plugin', 'list', '--marketplace', 'tools-codex', '--json'])
    if result.returncode:
        return found
    try:
        listing = json.loads(result.stdout)
        entries = listing['installed']
        if not isinstance(entries, list):
            raise ValueError
        seen = set()
        for entry in entries:
            name = entry.get('name')
            if name not in FILES:
                continue
            if name in seen:
                raise ValueError
            seen.add(name)
            release = entry.get('version', '')
            if (entry.get('installed') is not True or entry.get('enabled') is not True
                    or entry.get('marketplaceName') != 'tools-codex'
                    or entry.get('pluginId') != name + '@tools-codex'
                    or not re.fullmatch(r'\d+\.\d+\.\d+(?:\+[A-Za-z0-9.-]+)?', release)):
                continue
            candidate = package(home / 'plugins/cache/tools-codex' / name / release / 'skills' / name, name)
            if name not in found and candidate is not None:
                found[name] = candidate
    except (KeyError, TypeError, ValueError):
        raise ScheduleError('Liste des composants installés invalide') from None
    return found


def process_active(executable, arguments, terminal):
    """Un serveur/worker seul ne prouve pas la présence d'une interface."""
    executable = Path(executable)
    if executable.name.lower() not in ('codex', 'codex-desktop'):
        return False
    if any(arg.startswith('--type=') for arg in arguments[1:]):
        return False
    commands = {'app-server', 'exec', 'e', 'plugin', 'features', 'login', 'logout',
                'debug', 'mcp', 'mcp-server', 'review', 'queue', 'cloud', 'completion'}
    if any(arg in commands or arg in ('--help', '-h', '--version', '-V') for arg in arguments[1:]):
        return False
    desktop = (executable.name in ('Codex', 'codex-desktop') or
               executable.parent.name.lower() in ('codex', 'codex-desktop'))
    return desktop or terminal.startswith(('/dev/pts/', '/dev/tty'))


def codex_active(proc=Path('/proc'), uid=None):
    uid = os.getuid() if uid is None else uid
    parents = {}
    frontends = set()
    backends = set()
    for entry in proc.iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            if entry.stat().st_uid != uid:
                continue
            pid = int(entry.name)
            fields = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            parents[pid] = int(fields[1])
            executable = os.readlink(entry / 'exe')
            name = Path(executable).name.lower()
            if name not in ('codex', 'codex-desktop', 'chatgpt'):
                continue
            raw = (entry / 'cmdline').read_bytes()[:65536]
            arguments = [part.decode(errors='replace') for part in raw.split(b'\0') if part]
            try:
                terminal = os.readlink(entry / 'fd/0')
            except OSError:
                terminal = ''
            if process_active(executable, arguments, terminal):
                return True
            if name == 'chatgpt' and not any(arg.startswith('--type=') for arg in arguments[1:]):
                frontends.add(pid)
            if name == 'codex' and 'app-server' in arguments[1:]:
                backends.add(pid)
        except (OSError, ValueError, IndexError):
            continue
    # L'interface unifiée fournit un backend enfant ; un daemon isolé ne suffit pas.
    for pid in backends:
        visited = set()
        while pid in parents and pid not in visited:
            visited.add(pid)
            pid = parents[pid]
            if pid in frontends:
                return True
    return False


def quota_state(payload):
    """Ne conserver que les fenêtres Codex ; ni Spark, ni compte/crédits."""
    if not isinstance(payload, dict):
        return 'unknown'
    buckets = payload.get('rateLimitsByLimitId')
    if isinstance(buckets, dict) and buckets:
        bucket = buckets.get('codex')
    else:
        bucket = payload.get('rateLimits')
    if not isinstance(bucket, dict) or bucket.get('limitId') != 'codex':
        return 'unknown'
    windows = [bucket[key] for key in ('primary', 'secondary') if bucket.get(key) is not None]
    if not windows:
        return 'unknown'
    unknown = False
    exhausted = bool(bucket.get('rateLimitReachedType'))
    for window in windows:
        value = window.get('usedPercent') if isinstance(window, dict) else None
        if type(value) not in (float, int) or not math.isfinite(value) or value < 0:
            unknown = True
        elif value >= 100:
            exhausted = True
    return 'exhausted' if exhausted else 'unknown' if unknown else 'available'


def read_codex_quota(codex, home, timeout=30, popen=subprocess.Popen):
    environment = dict(os.environ, CODEX_HOME=str(home))
    process = None
    try:
        process = popen([str(codex), '-c', 'analytics.enabled=false', 'app-server', '--stdio'],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                        env=environment)
        def send(value):
            process.stdin.write(json.dumps(value).encode() + b'\n')
            process.stdin.flush()
        send({'id': 1, 'method': 'initialize', 'params': {
            'clientInfo': {'name': 'tools_codex_scheduler', 'version': '1'}}})
        buffer = b''
        received = 0
        expected = 1
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while time.monotonic() < deadline:
                if not selector.select(max(0, deadline - time.monotonic())):
                    break
                chunk = os.read(process.stdout.fileno(), 65536)
                received += len(chunk)
                if not chunk or received > LIMIT:
                    break
                buffer += chunk
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    message = json.loads(line)
                    if not isinstance(message, dict) or message.get('id') != expected:
                        continue
                    if 'error' in message or 'result' not in message:
                        return 'unknown'
                    if expected == 2:
                        return quota_state(message['result'])
                    send({'method': 'initialized'})
                    send({'id': 2, 'method': 'account/rateLimits/read'})
                    expected = 2
    except (OSError, ValueError, subprocess.SubprocessError):
        return 'unknown'
    finally:
        if process is not None:
            if process.stdin:
                try:
                    process.stdin.close()
                except BrokenPipeError:
                    pass
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            if process.stdout:
                process.stdout.close()
    return 'unknown'


@contextmanager
def lock(path, shared=False):
    path = safe(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(descriptor, (fcntl.LOCK_SH if shared else fcntl.LOCK_EX) | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ScheduleError('Opération déjà en cours') from None
        yield
    finally:
        os.close(descriptor)


def quote_unit(value, executable=False):
    value = str(value)
    if any(c in value for c in ('\n', '\r', '\x00')):
        raise ScheduleError('Chemin non conforme')
    value = value.replace('%', '%%').replace('\\', '\\\\').replace('"', '\\"')
    if executable:
        value = value.replace('$', '$$')
    return '"' + value + '"'


def layout(home, config_home):
    base = safe(home / 'llm-refresh')
    units = safe(config_home / 'systemd/user')
    return base, [base / 'scheduler.py', base / 'config.json',
                  units / (UNIT + '.service'), units / (UNIT + '.timer')]


def installed_config(home, config_home):
    base, paths = layout(home, config_home)
    receipt = base / 'manifest.json'
    if not receipt.exists():
        if any(p.exists() for p in paths):
            raise ScheduleError('Installation étrangère sans reçu')
        return None
    data = read_json(receipt)
    hashes = data.get('files')
    if data.get('schema_version') != 1 or not isinstance(hashes, dict) or set(hashes) != {str(p) for p in paths}:
        raise ScheduleError('Reçu du planning non conforme')
    for path in paths:
        safe(path)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != hashes[str(path)]:
            raise ScheduleError('Fichier du planning modifié ou absent')
    config = read_json(base / 'config.json')
    if (config.get('schema_version') != 1 or config.get('home') != str(home)
            or config.get('config_home') != str(config_home)
            or not isinstance(config.get('roots'), list)):
        raise ScheduleError('Configuration du planning non conforme')
    return config


def install(home=None, roots=(), config_home=None, apply=True, runner=command, source=None, codex=None):
    home = safe(home or home_path())
    config_home = safe(config_home or config_path())
    codex = codex or shutil.which('codex')
    found = discover(home, roots, runner, codex)
    if len(found) != 2:
        return {'status': 'composants_absents', 'cause': 'TFL et PLLM installés sont nécessaires'}
    if not codex:
        raise ScheduleError('CLI Codex indisponible')
    base, paths = layout(home, config_home)
    current = installed_config(home, config_home)
    configuration = {'schema_version': 1, 'home': str(home), 'config_home': str(config_home),
                     'roots': [str(Path(p).absolute()) for p in roots],
                     'python': str(Path(sys.executable).resolve()), 'codex': str(Path(codex).absolute())}
    executable = ' '.join(quote_unit(v, True) for v in
                          (configuration['python'], '-B', paths[0], 'run', '--home', home,
                           '--config-home', config_home))
    service = (MARKER + '[Unit]\nDescription=Tools Codex TFL puis PLLM\n\n[Service]\nType=oneshot\n'
               + 'Environment=' + quote_unit('CODEX_HOME=' + str(home)) + '\n'
               + 'Environment=' + quote_unit('XDG_RUNTIME_DIR=/run/user/' + str(os.getuid())) + '\n'
               + 'Environment=' + quote_unit('DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/' + str(os.getuid()) + '/bus') + '\n'
               + 'ExecStart=' + executable + '\nTimeoutStartSec=7500\nUMask=0077\n'
               + 'StandardOutput=null\nStandardError=null\n')
    timer = (MARKER + '[Unit]\nDescription=Tools Codex à 00 h et 12 h Paris\n\n[Timer]\n'
             + 'OnCalendar=' + CALENDAR + '\nPersistent=false\nAccuracySec=1s\n'
             + 'Unit=' + UNIT + '.service\n\n[Install]\nWantedBy=timers.target\n')
    content = [Path(source or __file__).read_bytes(), encoded(configuration), service.encode(), timer.encode()]
    changed = current is None or any(path.read_bytes() != data for path, data in zip(paths, content))
    if not apply:
        return {'status': 'a_installer' if current is None else 'a_mettre_a_jour' if changed else 'courant'}
    with lock(base / 'operation.lock'):
        # Revalider après le verrou : plusieurs hooks peuvent démarrer ensemble.
        installed_config(home, config_home)
        saved = {p: p.read_bytes() if p.exists() else None for p in [*paths, base / 'manifest.json']}
        try:
            for path, data in zip(paths, content):
                if not path.exists() or path.read_bytes() != data:
                    atomic_write(path, data)
            receipt = encoded({'schema_version': 1, 'files': {
                str(path): hashlib.sha256(data).hexdigest() for path, data in zip(paths, content)}})
            if not (base / 'manifest.json').exists() or (base / 'manifest.json').read_bytes() != receipt:
                atomic_write(base / 'manifest.json', receipt)
            if changed and runner(['systemctl', '--user', 'daemon-reload']).returncode:
                raise ScheduleError('Rechargement systemd utilisateur impossible')
            enabled = runner(['systemctl', '--user', 'is-enabled', UNIT + '.timer']).returncode == 0
            active = runner(['systemctl', '--user', 'is-active', UNIT + '.timer']).returncode == 0
            if not (enabled and active):
                if runner(['systemctl', '--user', 'enable', '--now', UNIT + '.timer']).returncode:
                    raise ScheduleError('Activation du timer utilisateur impossible')
            return {'status': 'installe' if current is None else 'mis_a_jour' if changed else 'courant',
                    'horaire': '00:00 et 12:00 Europe/Paris'}
        except (OSError, ScheduleError):
            if current is None:
                try:
                    runner(['systemctl', '--user', 'disable', '--now', UNIT + '.timer'])
                except ScheduleError:
                    pass
            for path, data in saved.items():
                if data is not None:
                    atomic_write(path, data)
                elif path.exists():
                    safe(path).unlink()
            runner(['systemctl', '--user', 'daemon-reload'])
            raise


def remove(home=None, config_home=None, runner=command):
    home = safe(home or home_path())
    config_home = safe(config_home or config_path())
    base, paths = layout(home, config_home)
    if installed_config(home, config_home) is None:
        return {'status': 'absent'}
    with lock(base / 'operation.lock'):
        installed_config(home, config_home)
        if runner(['systemctl', '--user', 'disable', '--now', UNIT + '.timer']).returncode:
            raise ScheduleError('Arrêt du timer utilisateur impossible')
        for path in [*paths, base / 'manifest.json']:
            safe(path).unlink()
        if runner(['systemctl', '--user', 'daemon-reload']).returncode:
            raise ScheduleError('Rechargement systemd utilisateur impossible après retrait')
    return {'status': 'retire'}


def run_refresh(home=None, config_home=None, runner=command, quota_reader=read_codex_quota,
                activity=codex_active):
    home = safe(home or home_path())
    config_home = safe(config_home or config_path())
    base, _ = layout(home, config_home)
    configuration = installed_config(home, config_home)
    if configuration is None:
        raise ScheduleError('Planning non installé')
    def finish(status, **fields):
        value = {'status': status, 'observed_at': datetime.now(timezone.utc).isoformat(timespec='seconds'), **fields}
        atomic_write(base / 'state.json', encoded(value))
        return value
    try:
        with lock(base / 'operation.lock'), lock(home / 'tcu.lock', shared=True):
            if not activity():
                return finish('ignore_codex_ferme')
            codex = configuration['codex']
            quota = quota_reader(codex, home)
            if quota != 'available':
                return finish('ignore_quota_epuise' if quota == 'exhausted' else 'ignore_quota_inconnu', etape='tfl')
            found = discover(home, configuration['roots'], runner, codex)
            if len(found) != 2:
                return finish('ignore_composants_absents')
            catalog = safe(found['tfl'] / 'data/tfl.json')
            before = catalog.stat().st_mtime_ns if catalog.exists() else None
            try:
                result = runner([configuration['python'], '-B', str(found['tfl'] / 'scripts' / FILES['tfl']),
                                 '--policy', 'auto', '--output-dir', str(catalog.parent)],
                                timeout=SCRIPT_TIMEOUT, cwd=found['tfl'])
            except ScheduleError:
                return finish('echec_tfl', cause='Exécution indisponible ou délai dépassé')
            if result.returncode:
                return finish('echec_tfl', code=result.returncode)
            if not catalog.is_file() or catalog.stat().st_mtime_ns == before:
                return finish('catalogue_non_actualise')
            try:
                data = read_json(catalog)
            except (OSError, ScheduleError):
                return finish('catalogue_non_valide')
            if not all(isinstance(data.get(key), dict) and isinstance(data[key].get('models'), list)
                       and data[key]['models'] for key in ('opencode_go', 'openrouter')):
                return finish('catalogue_non_valide')
            if not activity():
                return finish('ignore_codex_ferme', etape='pllm')
            quota = quota_reader(codex, home)
            if quota != 'available':
                return finish('ignore_quota_epuise' if quota == 'exhausted' else 'ignore_quota_inconnu', etape='pllm')
            try:
                result = runner([configuration['python'], '-B', str(found['pllm'] / 'scripts' / FILES['pllm']),
                                 '--tfl-catalog', str(catalog)], timeout=SCRIPT_TIMEOUT, cwd=found['pllm'])
            except ScheduleError:
                return finish('echec_pllm', cause='Exécution indisponible ou délai dépassé')
            return finish('succes' if result.returncode == 0 else 'echec_pllm', code=result.returncode)
    except ScheduleError as error:
        if str(error) == 'Opération déjà en cours':
            return {'status': 'ignore_occupe'}
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description='Planning utilisateur TFL puis PLLM')
    parser.add_argument('action', choices=('install', 'check', 'remove', 'run'))
    parser.add_argument('--home', type=Path)
    parser.add_argument('--config-home', type=Path)
    parser.add_argument('--skills-root', type=Path, action='append', default=[])
    parser.add_argument('--hook', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.action in ('install', 'check'):
            result = install(args.home, args.skills_root, args.config_home, apply=args.action == 'install')
        elif args.action == 'remove':
            result = remove(args.home, args.config_home)
        else:
            result = run_refresh(args.home, args.config_home)
        if not args.hook:
            print(json.dumps(result, ensure_ascii=False))
        return 1 if (result['status'].startswith('echec_') or
                     result['status'] in ('catalogue_non_actualise', 'catalogue_non_valide')) else 0
    except ScheduleError as error:
        if args.hook and str(error) == 'Opération déjà en cours':
            return 0
        # Le hook ne bloque pas le démarrage Codex ; le diagnostic reste filtré.
        print('Tools Codex : planning non disponible ; vérifier installation et session systemd utilisateur.', file=sys.stderr)
        return 1
    except OSError:
        print('Tools Codex : fichiers ou session utilisateur non disponibles.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
