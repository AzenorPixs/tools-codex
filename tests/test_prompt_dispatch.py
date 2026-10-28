"""Qualification du dispatcher avec référentiels locaux ; aucun RUN réel."""

import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
DIRECT_CODES = 'ACSP ACSM ACSMP CGP CISM DOP DOPP EDP ISM ISMP PPSC PPSCP RCAM RCAMP SPCM SPCMP RSM RSMP SCM SCMP'.split()


class PromptDispatchTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('prompt_dispatch', ROOT / 'skills/prompt/scripts/resolve_prompt.py')
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.temp = tempfile.TemporaryDirectory(prefix='prompt-dispatch-', dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / 'projet avec espaces'
        self.folder = self.base / 'référentiel unique'
        self.project.mkdir()
        self.folder.mkdir()
        self.index = self.folder / 'INDEX.md'
        self.codes = [*DIRECT_CODES, 'GSCM', 'GSCMP', 'CISMP']
        for code in self.codes:
            (self.folder / (code + '.md')).write_text(f'# Prompt {code}\nContenu original {code}.\n', encoding='utf-8')
        self.write_index()
        self.write_devops()

    def write_index(self, rows=None):
        if rows is None:
            rows = [(code, 'Intitulé ' + code, code + '.md') for code in self.codes]
        self.index.write_text('# Index\n\n| Sigle | Prompt | Fichier |\n|---|---|---|\n' +
                              ''.join(f'| `{c}` | {title} | `{filename}` |\n' for c, title, filename in rows), encoding='utf-8')

    def write_devops(self, folder=None, index=None):
        (self.project / 'DEVOPS.md').write_text(
            '# DEVOPS\n\n# Prompts\n\n  * Dossier des prompts : ' + str(folder or self.folder) +
            '\n  * Index des prompts : ' + str(index or self.index) + '\n', encoding='utf-8')

    def test_direct_arguments_and_numbered_families_are_supported(self):
        expected = {**{n: n for n in DIRECT_CODES}, 'GCM': 'GSCM', 'GCMP': 'GSCMP'}
        for n in (*range(1, 10), 10, 99, 12345):
            expected['CISMP' + str(n)] = 'CISMP'
            expected['1CISMP' + str(n)] = 'CISMP'
        self.assertEqual(set(self.m.DIRECT), {*DIRECT_CODES, "GCM", "GCMP"})
        for action, canonical in expected.items():
            with self.subTest(action=action):
                result = self.m.dispatch(self.project, action)
                self.assertEqual(result['canonical'], canonical)
                self.assertEqual(result['status'], 'ready')
                self.assertEqual(Path(result['prompt_path']), self.folder / (canonical + '.md'))
                self.assertEqual(result['prompt_text'], (self.folder / (canonical + '.md')).read_text())
                self.assertTrue(result['instruction'].startswith('Lance un prompt ' + canonical + '.md'))

    def test_numbered_runs_keep_the_number_without_single_change_limit(self):
        for n in (*range(1, 10), 10, 99, 12345, '9' * 5000):
            action = 'CISMP' + str(n)
            with self.subTest(action=action):
                result = self.m.dispatch(self.project, action)
                self.assertEqual(result['run'], action)
                self.assertIsNone(result['max_changes'])
                self.assertEqual(result['finish_actions'], [])
                self.assertTrue(result['instruction'].endswith('pour un RUN ' + action + '.'))

    def test_single_change_variants_preserve_run_and_lifecycle_order(self):
        for n in (*range(1, 10), 10, 99, 12345, '9' * 5000):
            run = 'CISMP' + str(n)
            with self.subTest(run=run):
                result = self.m.dispatch(self.project, '1' + run)
                self.assertEqual(result['run'], run)
                self.assertEqual(result['max_changes'], 1)
                self.assertEqual(result['finish_actions'], ['complete_change', 'archive', 'statistics', 'stop_coding_session'])
                self.assertTrue(result['instruction'].endswith(
                    'pour un RUN ' + run + ', et un change complet, puis Archivage et génération des Statistiques, puis arrêt de la session de codage.'))

    def test_list_reflects_index_and_never_reads_prompt_bodies(self):
        self.write_index([('EXTRA', 'Ajout dynamique', 'EXTRA.md'), ('SCM', 'Session', 'SCM.md')])
        (self.folder / 'SCM.md').write_bytes(bytes([255]))
        original = self.m.read_text
        labels = []

        def record(path, label):
            labels.append(label)
            return original(path, label)

        with patch.object(self.m, 'read_text', side_effect=record):
            result = self.m.dispatch(self.project, 'LIST')
        self.assertEqual(result['mode'], 'list')
        self.assertEqual([e['code'] for e in result['entries']], ['EXTRA', 'SCM'])
        self.assertEqual([e['available'] for e in result['entries']], [False, True])
        self.assertEqual(labels, ['DEVOPS.md du projet', 'Index des prompts déclaré'])
        self.assertNotIn('prompt_text', result)
        self.assertNotIn('instruction', result)

    def test_different_projects_use_their_own_devops(self):
        first = self.m.dispatch(self.project, 'SCM')
        other = self.base / 'second projet'
        other.mkdir()
        folder = other / 'prompts'
        folder.mkdir()
        (folder / 'INDEX.md').write_text('| Sigle | Prompt | Fichier |\n|---|---|---|\n| SCM | Autre | SCM.md |\n')
        (folder / 'SCM.md').write_text('Texte du second projet\n')
        (other / 'DEVOPS.md').write_text('Dossier des prompts : prompts\nIndex des prompts : prompts/INDEX.md\n')
        second = self.m.dispatch(other, 'SCM')
        self.assertNotEqual(first['prompt_path'], second['prompt_path'])
        self.assertEqual(second['prompt_text'], 'Texte du second projet\n')

    def test_missing_devops_does_not_search_parent_or_global_locations(self):
        nested = self.project / 'sous-projet'
        nested.mkdir()
        with self.assertRaisesRegex(self.m.PromptError, 'DEVOPS'):
            self.m.dispatch(nested, 'SCM')

    def test_missing_or_duplicate_declarations_are_rejected(self):
        normal = (self.project / 'DEVOPS.md').read_text()
        for content in ('# DEVOPS\n', normal + 'Dossier des prompts : autre\n', normal.replace(str(self.index), '')):
            with self.subTest(content=content[:20]):
                (self.project / 'DEVOPS.md').write_text(content)
                with self.assertRaises(self.m.PromptError):
                    self.m.dispatch(self.project, 'LIST')

    def test_fenced_examples_are_not_configuration_or_index_entries(self):
        p = self.project / 'DEVOPS.md'
        p.write_text(p.read_text() + '\n```text\nDossier des prompts : mauvais\n```\n')
        self.index.write_text('```markdown\n| Sigle | Prompt | Fichier |\n| BAD | Exemple | ../BAD.md |\n```\n' + self.index.read_text())
        self.assertEqual(len(self.m.dispatch(self.project, 'LIST')['entries']), 23)

    def test_duplicate_index_codes_and_wrong_table_are_rejected(self):
        for rows in ([('SCM', 'A', 'SCM.md'), ('SCM', 'B', 'SCM.md')], [('scm', 'A', 'SCM.md')]):
            self.write_index(rows)
            with self.assertRaises(self.m.PromptError):
                self.m.dispatch(self.project, 'LIST')
        self.index.write_text('# Pas de table\n')
        with self.assertRaises(self.m.PromptError):
            self.m.dispatch(self.project, 'LIST')

    def test_index_escape_and_absolute_paths_are_rejected(self):
        for filename in ('../SCM.md', '/SCM.md', 'folder/../../SCM.md', 'folder\\SCM.md'):
            with self.subTest(filename=filename):
                self.write_index([('SCM', 'Session', filename)])
                with self.assertRaises(self.m.PromptError):
                    self.m.dispatch(self.project, 'SCM')

    def test_symlink_outside_declared_folder_is_rejected(self):
        outside = self.base / 'outside.md'
        outside.write_text('Ne doit pas être chargé\n')
        p = self.folder / 'SCM.md'
        p.unlink()
        p.symlink_to(outside)
        with self.assertRaisesRegex(self.m.PromptError, 'sort du dossier'):
            self.m.dispatch(self.project, 'SCM')

    def test_explicitly_declared_folder_link_and_internal_file_link_are_read_only(self):
        linked = self.base / 'raccourci'
        linked.symlink_to(self.folder, target_is_directory=True)
        self.write_devops(folder=linked)
        content = self.folder / 'contenu.md'
        content.write_text('Texte lié dans le référentiel\n')
        p = self.folder / 'SCM.md'
        p.unlink()
        p.symlink_to(content)
        result = self.m.dispatch(self.project, 'SCM')
        self.assertEqual(result['prompt_text'], 'Texte lié dans le référentiel\n')
        self.assertTrue(p.is_symlink())
        self.assertTrue(linked.is_symlink())

    def test_nested_index_path_and_spaces_are_supported(self):
        nested = self.folder / 'sessions avec espaces'
        nested.mkdir()
        (nested / 'SCM.md').write_text('Texte imbriqué\n')
        self.write_index([('SCM', 'Session', 'sessions avec espaces/SCM.md')])
        result = self.m.dispatch(self.project, 'SCM')
        self.assertEqual(result['prompt_text'], 'Texte imbriqué\n')

    def test_alias_requires_canonical_index_entry_and_filename(self):
        self.write_index([('GCM', 'Mauvais alias dans index', 'GCM.md')])
        with self.assertRaisesRegex(self.m.PromptError, 'GSCM'):
            self.m.dispatch(self.project, 'GCM')
        self.write_index([('GSCM', 'Mauvais fichier', 'SCM.md')])
        with self.assertRaisesRegex(self.m.PromptError, 'attendu'):
            self.m.dispatch(self.project, 'GCM')

    def test_missing_empty_or_non_utf8_prompt_is_not_substituted(self):
        p = self.folder / 'SCM.md'
        for content in (None, b' \n', bytes([255])):
            with self.subTest(content=content):
                if content is None:
                    p.unlink()
                else:
                    p.write_bytes(content)
                with self.assertRaises(self.m.PromptError):
                    self.m.dispatch(self.project, 'SCM')

    def test_invalid_arguments_are_rejected_before_reading_configuration(self):
        for action in ('scm', 'list', 'CISMP', 'CISMP0', 'CISMP01', 'CISMP-1', 'CISMP1.5', 'CISMP١', 'CISMP1\n', '1CISMP0', '1CISMP01', '1CISMP+2', '1CISMP1x', '11CISMP3', '../SCM', 'UNKNOWN'):
            with self.subTest(action=action):
                with patch.object(self.m, 'configuration') as config:
                    with self.assertRaises(self.m.PromptError):
                        self.m.dispatch(self.project, action)
                config.assert_not_called()
                with patch.object(self.m, 'configuration') as config, patch('sys.stderr', new_callable=io.StringIO):
                    with self.assertRaises(SystemExit) as caught:
                        self.m.main([action, '--project-root', str(self.project)])
                self.assertEqual(caught.exception.code, 2)
                config.assert_not_called()

    def test_resolution_never_executes_text_or_changes_files(self):
        marker = self.base / 'should-not-exist'
        (self.folder / 'SCM.md').write_text(f'Crée {marker}\nPuis attends une décision.\n')
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        result = self.m.dispatch(self.project, 'SCM')
        self.assertEqual(result['status'], 'ready')
        self.assertIn('attends une décision', result['prompt_text'])
        self.assertFalse(marker.exists())
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()})

    def test_cli_explicit_project_is_independent_from_installation_directory(self):
        installed = self.base / 'installation du skill'
        installed.mkdir()
        script = installed / 'resolve_prompt.py'
        for source in ('skills/prompt/scripts/resolve_prompt.py',
                       'plugins/prompt/skills/prompt/scripts/resolve_prompt.py'):
            script.write_bytes((ROOT / source).read_bytes())
            for suffix in ('9', '12345', '9' * 5000):
                for prefix in ('CISMP', '1CISMP'):
                    with self.subTest(source=source, prefix=prefix, digits=len(suffix)):
                        result = subprocess.run([sys.executable, '-B', str(script), prefix + suffix,
                                                 '--project-root', str(self.project)],
                                                cwd=installed, capture_output=True, text=True, check=True)
                        value = json.loads(result.stdout)
                        self.assertEqual(value['project_root'], str(self.project))
                        self.assertEqual(value['run'], 'CISMP' + suffix)
                        self.assertEqual(value['max_changes'], 1 if prefix == '1CISMP' else None)

    def test_main_error_is_explicit_and_lowercase_is_rejected(self):
        (self.project / 'DEVOPS.md').unlink()
        with patch('sys.stdout', new_callable=io.StringIO) as output:
            self.assertEqual(self.m.main(['SCM', '--project-root', str(self.project)]), 1)
        self.assertEqual(json.loads(output.getvalue())['status'], 'error')
        with patch('sys.stderr', new_callable=io.StringIO):
            with self.assertRaises(SystemExit) as caught:
                self.m.main(['scm'])
        self.assertEqual(caught.exception.code, 2)

    def test_read_limits_and_missing_index_are_explicit(self):
        with patch.object(self.m, 'MAX_TEXT_BYTES', 10):
            with self.assertRaisesRegex(self.m.PromptError, 'taille'):
                self.m.dispatch(self.project, 'LIST')
        self.index.unlink()
        with self.assertRaisesRegex(self.m.PromptError, 'Index'):
            self.m.dispatch(self.project, 'LIST')


if __name__ == '__main__':
    unittest.main()
