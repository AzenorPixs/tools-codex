"""Liste noire LM commune aux paquets autonomes ; aucun effet à l'import."""

from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile


DEFAULT_MODELS = ('mimo-v2.5',)
PERMANENT_MODELS = ('muse-spark-1.2-contributor',)
MAX_BYTES = 64 * 1024


class BlacklistError(RuntimeError):
    """Échec de politique LM, sans contenu du fichier dans le diagnostic."""


def policy_path() -> Path:
    base = Path(os.environ['CODEX_HOME']) if os.environ.get('CODEX_HOME') else Path.home() / '.codex'
    return base / 'lm' / 'blacklist.json'


def canonical_id(value: str) -> str:
    if (not isinstance(value, str) or len(value) > 256
            or not re.fullmatch(
                r'(?:~(?=[A-Za-z0-9][A-Za-z0-9._-]*/))?'
                r'[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)*(?::[A-Za-z0-9][A-Za-z0-9._-]*)?', value)):
        raise BlacklistError('LM : identifiant de modèle invalide')
    model = value.lower().rsplit('/', 1)[-1]
    while model.endswith((':free', '-free')):
        model = model[:-5]
    if not model:
        raise BlacklistError('LM : identifiant de modèle vide')
    return model


def _pairs(items: list) -> dict:
    result = {}
    for key, value in items:
        if key in result:
            raise BlacklistError('LM : clé JSON dupliquée')
        result[key] = value
    return result


def load_models(path: Path | None = None) -> tuple[str, ...]:
    path = policy_path() if path is None else Path(path)
    try:
        if path.is_symlink():
            raise BlacklistError('LM : le fichier de politique ne peut pas être un lien')
        with path.open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
    except FileNotFoundError:
        return DEFAULT_MODELS
    except OSError as error:
        raise BlacklistError('LM : liste noire inaccessible') from error
    if len(raw) > MAX_BYTES:
        raise BlacklistError('LM : liste noire trop volumineuse')
    try:
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs)
    except (ValueError, UnicodeError) as error:
        raise BlacklistError('LM : liste noire JSON invalide') from error
    if (not isinstance(data, dict) or set(data) != {'schema_version', 'models'}
            or type(data['schema_version']) is not int or data['schema_version'] != 1
            or not isinstance(data['models'], list)):
        raise BlacklistError('LM : schéma de liste noire invalide')
    models = [canonical_id(value) for value in data['models']]
    if len(models) != len(set(models)):
        raise BlacklistError('LM : identifiant dupliqué dans la liste noire')
    return tuple(sorted(models))


def is_blocked(model_id: str, models: tuple[str, ...] | None = None) -> bool:
    configured = load_models() if models is None else models
    return canonical_id(model_id) in (*configured, *PERMANENT_MODELS)


def require_allowed(model_id: str, models: tuple[str, ...] | None = None) -> None:
    if is_blocked(model_id, models):
        raise BlacklistError('Modèle exclu par la liste noire LM ou permanente')


@contextmanager
def _writer_lock(path: Path):
    directory = path.parent
    if directory.is_symlink():
        raise BlacklistError('LM : le dossier de politique ne peut pas être un lien')
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    flags = os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW
    descriptor = os.open(directory / 'blacklist.lock', flags, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise BlacklistError('LM : une modification est déjà en cours') from error
        yield
    finally:
        os.close(descriptor)


def update_models(action: str, model_id: str, path: Path | None = None) -> tuple[str, ...]:
    if action not in ('ADD', 'REMOVE'):
        raise BlacklistError('LM : action de modification inconnue')
    model = canonical_id(model_id)
    path = policy_path() if path is None else Path(path)
    temporary = None
    try:
        with _writer_lock(path):
            current = load_models(path)
            models = set(current)
            if action == 'ADD':
                models.add(model)
            else:
                models.discard(model)
            result = tuple(sorted(models))
            if result == current and path.exists():
                return result
            raw = (json.dumps({'schema_version': 1, 'models': result}, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
            if len(raw) > MAX_BYTES:
                raise BlacklistError('LM : liste noire trop volumineuse')
            descriptor, name = tempfile.mkstemp(prefix='.blacklist-', dir=path.parent)
            temporary = Path(name)
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
            temporary = None
            return result
    except OSError as error:
        raise BlacklistError('LM : modification impossible, liste précédente préservée') from error
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
