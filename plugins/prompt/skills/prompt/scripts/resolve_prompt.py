#!/usr/bin/env python3
"""Résoudre un prompt depuis le DEVOPS du projet ; aucune action du prompt exécutée."""

import argparse
import json
from pathlib import Path, PurePosixPath
import re


MAX_TEXT_BYTES = 1024 * 1024
DIRECT = {name: name for name in (
    'ACSP', 'ACSM', 'ACSMP', 'CGP', 'CISM', 'DOP', 'DOPP', 'EDP', 'ISM', 'ISMP',
    'PPSC', 'PPSCP', 'RCAM', 'RCAMP', 'SPCM', 'SPCMP', 'RSM', 'RSMP', 'SCM', 'SCMP')}
DIRECT.update(GCM='GSCM', GCMP='GSCMP')
RUN_ACTION = re.compile(r'(1)?CISMP([1-9][0-9]*)')


class PromptError(Exception):
    """Configuration ou argument indisponible, sans recherche de repli."""


def read_text(path: Path, label: str) -> str:
    try:
        with path.open('rb') as stream:
            raw = stream.read(MAX_TEXT_BYTES + 1)
        if len(raw) > MAX_TEXT_BYTES:
            raise PromptError(f'{label} dépasse la taille autorisée')
        return raw.decode('utf-8')
    except UnicodeError as exc:
        raise PromptError(f'{label} doit être en UTF-8') from exc
    except OSError as exc:
        raise PromptError(f'{label} absent ou inaccessible') from exc


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '`':
        value = value[1:-1]
    return value


def resolved(path: Path, label: str) -> Path:
    try:
        return path.resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        raise PromptError(f'{label} ne peut pas être résolu') from exc


def declared_path(value: str, project: Path, label: str) -> Path:
    value = unquote(value)
    if (not value or any(ord(c) < 32 for c in value) or '$' in value or '`' in value):
        raise PromptError(f'{label} exige un chemin littéral non vide')
    path = Path(value)
    if not path.is_absolute():
        path = project / path
    return resolved(path, label)


def configuration(project_root: Path) -> tuple[Path, Path, Path]:
    project = resolved(project_root, 'Projet')
    if not project.is_dir():
        raise PromptError('Projet absent ou non répertoire')
    text = read_text(project / 'DEVOPS.md', 'DEVOPS.md du projet')
    labels = {'Dossier des prompts': [], 'Index des prompts': []}
    fence = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(('```', '~~~')):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        match = re.fullmatch(r'\s*(?:[-*+]\s+)?(Dossier des prompts|Index des prompts)\s*:\s*(.*?)\s*', line)
        if match:
            labels[match[1]].append(match[2])
    if any(len(values) != 1 or not values[0].strip() for values in labels.values()):
        raise PromptError('Dossier ou index des prompts absent ou ambigu dans DEVOPS.md')
    folder = declared_path(labels['Dossier des prompts'][0], project, 'Dossier des prompts')
    index = declared_path(labels['Index des prompts'][0], project, 'Index des prompts')
    if index.suffix.lower() != '.md':
        raise PromptError('L’index déclaré doit être un fichier Markdown')
    if not folder.is_dir():
        raise PromptError('Dossier des prompts absent ou inaccessible')
    return project, folder, index


def prompt_path(folder: Path, filename: str) -> Path:
    relative = PurePosixPath(filename)
    if (not filename or '\\' in filename or any(ord(c) < 32 for c in filename)
            or relative.is_absolute() or '..' in relative.parts or str(relative) != filename
            or relative.suffix != '.md' or any(part.startswith('.') for part in relative.parts)):
        raise PromptError('Chemin de prompt invalide dans l’index')
    path = resolved(folder / filename, 'Fichier de prompt')
    if not path.is_relative_to(folder):
        raise PromptError('Le fichier de prompt sort du dossier déclaré')
    return path


def index_entries(folder: Path, index: Path) -> list[dict]:
    text = read_text(index, 'Index des prompts déclaré')
    entries = []
    seen = set()
    table = False
    fence = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(('```', '~~~')):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            table = False
            continue
        if fence is not None:
            continue
        if not stripped.startswith('|') or not stripped.endswith('|'):
            table = False
            continue
        cells = [unquote(c).replace('\\|', '|') for c in re.split(r'(?<!\\)\|', stripped)[1:-1]]
        if [c.casefold() for c in cells] == ['sigle', 'prompt', 'fichier']:
            table = True
            continue
        if not table:
            continue
        if len(cells) == 3 and all(re.fullmatch(r':?-+:?', c) for c in cells):
            continue
        if len(cells) != 3:
            raise PromptError('Ligne de table de prompts invalide')
        code, title, filename = cells
        if not re.fullmatch('[A-Z][A-Z0-9]*', code) or not title or code in seen:
            raise PromptError('Sigle invalide ou dupliqué dans l’index')
        seen.add(code)
        path = prompt_path(folder, filename)
        entries.append({'code': code, 'title': title, 'file': filename,
                        'path': str(path), 'available': path.is_file()})
        if len(entries) > 512:
            raise PromptError('Index de prompts trop volumineux')
    if not entries:
        raise PromptError('Table Sigle / Prompt / Fichier absente ou vide dans l’index')
    return entries


def valid_action(action: str) -> bool:
    return action in DIRECT or action == 'LIST' or RUN_ACTION.fullmatch(action) is not None


def cli_action(action: str) -> str:
    if not valid_action(action):
        raise argparse.ArgumentTypeError('Code attendu en MAJUSCULE : LIST, code direct, CISMPx ou 1CISMPx (x entier positif sans zéro initial)')
    return action


def dispatch(project_root: Path, action: str) -> dict:
    if not valid_action(action):
        raise PromptError('Argument inconnu : utiliser un des codes en MAJUSCULE du skill')
    project, folder, index = configuration(project_root)
    entries = index_entries(folder, index)
    result = {'project_root': str(project), 'prompts_dir': str(folder),
              'index_path': str(index), 'argument': action}
    if action == 'LIST':
        return {**result, 'mode': 'list', 'status': 'listed', 'entries': entries}
    match = RUN_ACTION.fullmatch(action)
    run = 'CISMP' + match[2] if match else None
    single = bool(match and match[1])
    canonical = 'CISMP' if match else DIRECT[action]
    entry = next((e for e in entries if e['code'] == canonical), None)
    if entry is None:
        raise PromptError(f'Entrée {canonical} absente de l’index déclaré')
    if PurePosixPath(entry['file']).name != canonical + '.md':
        raise PromptError(f'Le fichier indexé ne correspond pas au prompt attendu {canonical}.md')
    if not entry['available']:
        raise PromptError(f'Prompt {canonical}.md absent ou inaccessible')
    body = read_text(Path(entry['path']), f'Prompt {canonical}.md')
    if not body.strip():
        raise PromptError(f'Prompt {canonical}.md vide')
    instruction = (f"Lance un prompt {canonical}.md jusqu'a état terminal et ne rendre la main "
                   "que si les conditions du prompts l'oblige")
    if run:
        instruction += f' pour un RUN {run}'
    if single:
        instruction += (', et un change complet, puis Archivage et génération des Statistiques, '
                        'puis arrêt de la session de codage')
    instruction += '.'
    return {**result, 'mode': 'execute', 'status': 'ready', 'canonical': canonical,
            'prompt_path': entry['path'], 'prompt_text': body, 'instruction': instruction,
            'run': run, 'max_changes': 1 if single else None,
            'finish_actions': ['complete_change', 'archive', 'statistics', 'stop_coding_session'] if single else []}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', type=cli_action, help='LIST, code direct, CISMPx ou 1CISMPx ; x entier positif sans borne supérieure')
    parser.add_argument('--project-root', type=Path, default=Path.cwd(), help='Racine réelle du projet courant')
    args = parser.parse_args(argv)
    try:
        result = dispatch(args.project_root, args.action)
    except PromptError as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
