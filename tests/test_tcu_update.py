"""Qualification hors ligne TCU : jamais de réseau ni de profil utilisateur réel."""

import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def load_script():
    spec = importlib.util.spec_from_file_location('tcu_under_test', ROOT / 'skills/tcu/scripts/update.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_files():
    files = {'VERSION': b'0.3.0\n', '.codex/commands/TCU.md': b'nouvelle commande\n'}
    entries = []
    for name in ('cm', 'tcu'):
        entries.append({'name': name, 'source': {'source': 'local', 'path': './plugins/' + name}})
        files[f'plugins/{name}/.codex-plugin/plugin.json'] = json.dumps({
            'name': name, 'version': '0.3.0', 'skills': './skills/'}).encode()
        files[f'skills/{name}/SKILL.md'] = (
            f'---\nname: {name}\ndescription: Catalogue de test\n---\nNouveau contenu\n').encode()
    files['skills/tcu/scripts/update.py'] = b'print("fixture uniquement")\n'
    files['.agents/plugins/marketplace.json'] = json.dumps({'name': 'tools-codex', 'plugins': entries}).encode()
    return files


def zip_bytes(files, extra=None):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        for name, data in files.items():
            archive.writestr('snapshot/' + name, data)
        if extra:
            archive.writestr(*extra)
    return stream.getvalue()


class TcuUpdateTests(unittest.TestCase):
    def setUp(self):
        self.m = load_script()
        self.tmp = tempfile.TemporaryDirectory(prefix='tcu-', dir=ROOT / 'tests')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / 'profil test'
        self.base.mkdir()
        self.home = self.base / 'codex'
        self.skills = self.base / 'skills'
        self.skills.mkdir()
        self.files = source_files()
        self.remote = self.m.snapshot(self.fetcher)
        # Les profils de test résident sous le dépôt pour respecter son périmètre.
        self.dev = patch.object(self.m, 'development', return_value=False)
        self.dev.start()
        self.addCleanup(self.dev.stop)
        self.before = {}
        self.after = None
        self.calls = []
        self.upgraded = False

    def fetcher(self, url):
        sha = getattr(self, 'source_sha', 'a' * 40)
        if url.endswith('/commits/HEAD'):
            return json.dumps({'sha': sha}).encode()
        self.assertTrue(url.endswith('/zipball/' + sha))
        return zip_bytes(self.files)

    def runner(self, args):
        self.calls.append(args)
        if args[0] == 'marketplace':
            self.assertEqual(args, ['marketplace', 'upgrade', 'tools-codex', '--json'])
            self.upgraded = True
            return {}
        if args[0] == 'add':
            self.assertEqual(args, ['add', 'prompt@tools-codex', '--json'])
            state = copy.deepcopy(self.after if self.after is not None else self.before)
            enabled = state.get('prompt', {}).get('enabled', True)
            state['prompt'] = self.prompt_entry('0.3.0', enabled)
            self.after = state
            self.prompt_cache('0.3.0')
            return {}
        self.assertEqual(args, ['list', '--marketplace', 'tools-codex', '--json'])
        return {'installed': list(copy.deepcopy(self.after if self.upgraded and self.after is not None else self.before).values())}

    def plugin(self, release='0.2.3', enabled=True):
        return {'name': 'cm', 'pluginId': 'cm@tools-codex', 'marketplaceName': 'tools-codex',
                'version': release, 'installed': True, 'enabled': enabled,
                'marketplaceSource': {'sourceType': 'git', 'source': self.m.REPO_URL + '.git'}}

    def cache(self, release, data=None):
        package = self.m.cache_root(self.home, 'cm', release)
        path = package / '.codex-plugin/plugin.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({'name': 'cm', 'version': release}))
        if data is not None:
            p = package / 'skills/cm/data/report.json'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        return package

    def enable_prompt(self):
        catalog = json.loads(self.files['.agents/plugins/marketplace.json'])
        catalog['plugins'].append({'name': 'prompt', 'source': {'source': 'local', 'path': './plugins/prompt'}})
        self.files['.agents/plugins/marketplace.json'] = json.dumps(catalog).encode()
        self.files['plugins/prompt/.codex-plugin/plugin.json'] = json.dumps({
            'name': 'prompt', 'version': '0.3.0', 'skills': './skills/'}).encode()
        self.files['skills/prompt/SKILL.md'] = b'---\nname: prompt\ndescription: Fixture\n---\nPrompt fixture\n'
        self.files['skills/prompt/scripts/resolve_prompt.py'] = b'raise RuntimeError("fixture must stay inactive")\n'
        self.files['.codex/commands/PROMPT.md'] = b'Utilise le skill prompt. Arguments: $ARGUMENTS\n'
        self.remote = self.m.snapshot(self.fetcher)

    def prompt_entry(self, release='0.3.0', enabled=True):
        entry = self.plugin(release, enabled)
        entry.update(name='prompt', pluginId='prompt@tools-codex')
        return entry

    def prompt_cache(self, release, complete=True):
        package = self.m.cache_root(self.home, 'prompt', release)
        manifest = package / '.codex-plugin/plugin.json'
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({'name': 'prompt', 'version': release, 'skills': './skills/'}))
        if complete:
            for name in ['skills/prompt/SKILL.md', 'skills/prompt/scripts/resolve_prompt.py']:
                path = package / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(self.files[name])
        return package

    def local(self, name='cm', content=b'ancien contenu\n', tracked=False):
        target = self.skills / name
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_bytes(content)
        if tracked:
            (target / self.m.RECEIPT).write_text(json.dumps({
                'schema': 1, 'repository': self.m.REPOSITORY, 'sha': 'b' * 40, 'version': '0.2.3',
                'hashes': {'SKILL.md': hashlib.sha256(content).hexdigest()}}))
        return target

    def execute(self, apply=False, adopt=False, roots=None):
        return self.m.execute(self.home, roots or [('skills', self.skills)], apply, adopt,
                              fetcher=self.fetcher, runner=self.runner)

    def enable_lm(self):
        catalog = json.loads(self.files['.agents/plugins/marketplace.json'])
        catalog['plugins'].append({'name': 'lm', 'source': {'source': 'local', 'path': './plugins/lm'}})
        self.files['.agents/plugins/marketplace.json'] = json.dumps(catalog).encode()
        self.files['plugins/lm/.codex-plugin/plugin.json'] = json.dumps({
            'name': 'lm', 'version': '0.3.0', 'skills': './skills/'}).encode()
        for path in (ROOT / 'skills/lm').rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                self.files[str(path.relative_to(ROOT))] = path.read_bytes()
        self.files['.codex/commands/LM.md'] = (ROOT / '.codex/commands/LM.md').read_bytes()

    def test_lm_absent_is_not_installed_and_common_policy_is_preserved(self):
        self.enable_lm()
        policy = self.home / 'lm/blacklist.json'
        policy.parent.mkdir(parents=True)
        policy.write_bytes(b'{"schema_version":1,"models":["custom"]}\n')
        content = policy.read_bytes()
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertFalse((self.skills / 'lm').exists())
        self.assertFalse(any(c[0] == 'add' for c in self.calls))
        self.assertEqual(policy.read_bytes(), content)
        self.assertTrue(any(r['brique'] == 'lm' and r['status'] == 'absent' for r in report['briques']))

    def test_lm_existing_autonomous_sources_update_without_changing_common_policy(self):
        self.enable_lm()
        target = self.local('lm', tracked=True)
        policy = self.home / 'lm/blacklist.json'
        policy.parent.mkdir(parents=True)
        policy.write_bytes(b'{"schema_version":1,"models":["custom"]}\n')
        content = policy.read_bytes()
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        for name in ('SKILL.md', 'scripts/lm.py', 'scripts/model_blacklist.py', 'agents/openai.yaml'):
            self.assertEqual((target / name).read_bytes(), self.files['skills/lm/' + name])
        self.assertEqual(policy.read_bytes(), content)
        self.assertEqual(json.loads((target / self.m.RECEIPT).read_text())['version'], '0.3.0')

    def test_actual_six_plugin_source_snapshot_includes_lm_and_shared_modules(self):
        files = {name:(ROOT/name).read_bytes() for name in ('VERSION','.agents/plugins/marketplace.json')}
        for path in (ROOT/'plugins').glob('*/.codex-plugin/plugin.json'):
            files[str(path.relative_to(ROOT))] = path.read_bytes()
        for path in (ROOT/'plugins').glob('*/hooks/hooks.json'):
            files[str(path.relative_to(ROOT))] = path.read_bytes()
        for path in (ROOT/'skills').rglob('*'):
            relative = path.relative_to(ROOT)
            if path.is_file() and self.m.source_file(self.m.PurePosixPath(*relative.parts[2:])):
                files[str(relative)] = path.read_bytes()
        for path in (ROOT/'.codex/commands').glob('*.md'):
            files[str(path.relative_to(ROOT))] = path.read_bytes()
        def fetch(url):
            return json.dumps({'sha':'a'*40}).encode() if url.endswith('/commits/HEAD') else zip_bytes(files)
        remote = self.m.snapshot(fetch)
        self.assertEqual(remote['version'],'0.7.20')
        self.assertEqual(remote['plugins'], {'cm','lm','tfl','pllm','prompt','tcu'})
        for name in ('lm','tfl','pllm'):
            self.assertIn('skills/'+name+'/scripts/model_blacklist.py',remote['files'])

    def test_check_has_no_writes_and_does_not_refresh(self):
        target = self.local(tracked=True)
        initial = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        report = self.execute()
        self.assertTrue(report['succes'])
        self.assertFalse(self.home.exists())
        self.assertFalse(self.upgraded)
        self.assertEqual(initial, {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()})
        row = next(r for r in report['briques'] if r['brique'] == str(target))
        self.assertEqual((row['avant'], row['apres'], row['cible']), ('0.2.3', '0.2.3', '0.3.0'))

    def test_untracked_difference_requires_explicit_adoption(self):
        target = self.local()
        result = self.execute(apply=True)
        self.assertFalse(result['succes'])
        self.assertTrue(self.upgraded)
        self.assertEqual((target / 'SKILL.md').read_bytes(), b'ancien contenu\n')
        self.assertFalse((target / self.m.RECEIPT).exists())

    def test_adoption_backs_up_and_preserves_data_and_configuration(self):
        target = self.local()
        (target / 'data').mkdir()
        (target / 'data/history.json').write_bytes(b'local history')
        (target / 'private.conf').write_bytes(b'fixture configuration')
        report = self.execute(apply=True, adopt=True)
        self.assertTrue(report['succes'])
        self.assertEqual((target / 'SKILL.md').read_bytes(), self.files['skills/cm/SKILL.md'])
        self.assertEqual((target / 'data/history.json').read_bytes(), b'local history')
        self.assertEqual((target / 'private.conf').read_bytes(), b'fixture configuration')
        backups = list(Path(report['backup']).rglob('SKILL.md'))
        self.assertEqual(stat.S_IMODE(Path(report['backup']).stat().st_mode), 0o700)
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), b'ancien contenu\n')
        receipt = json.loads((target / self.m.RECEIPT).read_text())
        self.assertEqual(receipt['version'], '0.3.0')
        self.assertEqual(receipt['repository'], self.m.REPOSITORY)

    def test_tracked_modification_cannot_be_forced_by_adoption(self):
        target = self.local(tracked=True)
        (target / 'SKILL.md').write_bytes(b'modification manuelle')
        result = self.execute(apply=True, adopt=True)
        self.assertFalse(result['succes'])
        self.assertTrue(self.upgraded)
        self.assertEqual((target / 'SKILL.md').read_bytes(), b'modification manuelle')

    def test_symbolic_links_and_development_checkout_are_not_updated(self):
        target = self.base / 'real'
        target.mkdir()
        (target / 'SKILL.md').write_bytes(b'local')
        (self.skills / 'cm').symlink_to(target, target_is_directory=True)
        self.assertFalse(self.execute(apply=True, adopt=True)['succes'])
        self.dev.stop()
        self.assertTrue(self.m.development(ROOT / 'skills/cm'))
        plan = self.m.local_plan(self.remote, [('skills', ROOT / 'skills')], True)
        self.assertTrue(any(p['status'] == 'conflit' for p in plan))
        self.assertEqual((target / 'SKILL.md').read_bytes(), b'local')

    def test_missing_bricks_are_not_installed(self):
        result = self.execute(apply=True)
        self.assertTrue(result['succes'])
        self.assertEqual(list(self.skills.iterdir()), [])
        self.assertTrue(all(r['status'] == 'absent' for r in result['briques']
                            if r.get('ressource') != 'planification'))
        schedule = next(r for r in result['briques'] if r.get('ressource') == 'planification')
        self.assertEqual(schedule['status'], 'composants_absents')
        self.assertFalse(any(c[0] == 'add' for c in self.calls))

    def test_schedule_check_is_planned_without_mutation_or_generation(self):
        with patch.object(self.m.scheduler, 'install', return_value={'status': 'a_installer'}) as install:
            report = self.execute()
        self.assertTrue(report['succes'])
        install.assert_called_once()
        self.assertFalse(install.call_args.kwargs['apply'])
        self.assertFalse(self.home.exists())
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'llm-refresh')['status'], 'a_installer')

    def test_schedule_apply_reports_bootstrap_separately(self):
        with patch.object(self.m.scheduler, 'install', return_value={'status': 'installe'}) as install:
            report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        install.assert_called_once()
        self.assertTrue(install.call_args.kwargs['apply'])
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'llm-refresh')['status'], 'installe')

    def test_schedule_failure_keeps_partial_update_and_returns_failure(self):
        with patch.object(self.m.scheduler, 'install', side_effect=self.m.scheduler.ScheduleError('Session indisponible')):
            report = self.execute(apply=True)
        self.assertFalse(report['succes'])
        self.assertTrue(self.upgraded)
        self.assertIn('Planning utilisateur', report['erreur'])
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'llm-refresh')['status'], 'incomplet')

    def test_schedule_does_not_arm_a_conflicting_tfl_or_pllm_source(self):
        for name in ('tfl', 'pllm'):
            plan = {'brique': str(self.skills / name), 'canal': 'github', 'status': 'conflit'}
            with patch.object(self.m, 'local_plan', return_value=[plan]):
                with patch.object(self.m.scheduler, 'install') as install:
                    report = self.execute(apply=True)
            install.assert_not_called()
            self.assertFalse(report['succes'])
            self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'llm-refresh')['status'], 'conflit')

    def test_unverified_hook_command_blocks_before_any_mutation(self):
        manifest = 'plugins/cm/.codex-plugin/plugin.json'
        data = json.loads(self.files[manifest])
        data['hooks'] = './hooks/hooks.json'
        self.files[manifest] = json.dumps(data).encode()
        self.files['skills/cm/scripts/scheduler.py'] = b'# fixture\n'
        for hooks in ({'hooks': {'SessionStart': [{'hooks': [{'type': 'command', 'command': 'fixture-untrusted'}]}]}},
                      {'hooks': []}):
            self.files['plugins/cm/hooks/hooks.json'] = json.dumps(hooks).encode()
            with self.assertRaises(self.m.UpdateError):
                self.m.snapshot(self.fetcher)
        self.assertFalse(self.home.exists())
        self.assertEqual(self.calls, [])

    def test_existing_commands_only_are_updated(self):
        commands = self.base / 'commands'
        commands.mkdir()
        (commands / 'TCU.md').write_bytes(b'ancienne commande')
        (commands / 'other.md').write_bytes(b'autre commande')
        report = self.execute(apply=True, adopt=True, roots=[('commands', commands)])
        self.assertTrue(report['succes'])
        self.assertEqual((commands / 'TCU.md').read_bytes(), self.files['.codex/commands/TCU.md'])
        self.assertEqual((commands / 'other.md').read_bytes(), b'autre commande')

    def test_self_update_adds_script_and_keeps_retired_managed_files(self):
        target = self.local('tcu', tracked=True)
        retired = target / 'old.py'
        retired.write_bytes(b'print(1)\n')
        p = target / self.m.RECEIPT
        receipt = json.loads(p.read_text())
        receipt['hashes']['old.py'] = self.m.digest(retired.read_bytes())
        p.write_text(json.dumps(receipt))
        result = self.execute(apply=True)
        self.assertTrue(result['succes'])
        self.assertEqual((target / 'scripts/update.py').read_bytes(), self.files['skills/tcu/scripts/update.py'])
        self.assertEqual(retired.read_bytes(), b'print(1)\n')

    def test_marketplace_versions_activation_and_data_are_verified(self):
        self.before = {'cm': self.plugin(enabled=False)}
        self.after = {'cm': self.plugin('0.3.0', enabled=False)}
        self.cache('0.2.3', b'local quotas')
        new = self.cache('0.3.0', b'distant sample')
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertEqual((new / 'skills/cm/data/report.json').read_bytes(), b'local quotas')
        row = next(r for r in report['briques'] if r['brique'] == 'cm' and r['canal'] == 'marketplace')
        self.assertEqual((row['avant'], row['apres'], row['status']), ('0.2.3', '0.3.0', 'mis_a_jour'))

    def test_marketplace_failure_is_partial_and_blocks_autonomous_writes(self):
        target = self.local(tracked=True)
        self.before = {'cm': self.plugin()}
        self.after = {'cm': self.plugin('0.3.0')}
        self.cache('0.2.3', b'local data')
        new = self.cache('0.3.0')
        original_runner = self.runner

        def failing(args):
            result = original_runner(args)
            if args[0] == 'marketplace':
                raise self.m.UpdateError('CLI échec simulé après rafraîchissement')
            return result

        with patch.object(self, 'runner', side_effect=failing):
            result = self.execute(apply=True)
        self.assertFalse(result['succes'])
        self.assertEqual((target / 'SKILL.md').read_bytes(), b'ancien contenu\n')
        self.assertEqual((new / 'skills/cm/data/report.json').read_bytes(), b'local data')
        row = next(r for r in result['briques'] if r['brique'] == 'cm')
        self.assertEqual(row['apres'], '0.3.0')

    def test_version_or_activation_mismatch_blocks_sources(self):
        target = self.local(tracked=True)
        self.before = {'cm': self.plugin()}
        self.cache('0.2.3')
        self.cache('0.3.0')
        for after in (self.plugin(), self.plugin('0.3.0', enabled=False)):
            with self.subTest(after=after):
                self.upgraded = False
                self.after = {'cm': after}
                result = self.execute(apply=True)
                self.assertFalse(result['succes'])
                self.assertEqual((target / 'SKILL.md').read_bytes(), b'ancien contenu\n')

    def test_unverifiable_plugin_data_blocks_refresh(self):
        self.before = {'cm': self.plugin()}
        package = self.cache('0.2.3')
        data = package / 'skills/cm/data'
        data.mkdir(parents=True)
        (data / 'unknown.bin').write_bytes(b'unsupported fixture')
        result = self.execute(apply=True)
        self.assertFalse(result['succes'])
        self.assertFalse(self.upgraded)

    def test_failed_post_refresh_read_does_not_invent_versions(self):
        self.before = {'cm': self.plugin()}
        self.cache('0.2.3')
        original = self.runner

        def broken(args):
            if self.upgraded and args[0] == 'list':
                raise self.m.UpdateError('liste inaccessible')
            return original(args)

        with patch.object(self, 'runner', side_effect=broken):
            report = self.execute(apply=True)
        self.assertFalse(report['succes'])
        row = next(r for r in report['briques'] if r['brique'] == 'cm')
        self.assertIsNone(row['apres'])
        self.assertEqual(row['status'], 'inconnu')

    def test_rollback_restores_prior_sources_and_receipt(self):
        target = self.local('tcu', tracked=True)
        old_receipt = (target / self.m.RECEIPT).read_bytes()
        plans = self.m.local_plan(self.remote, [('skills', self.skills)], False)
        count = 0

        def failing(path, data):
            nonlocal count
            count += 1
            self.m.atomic_write(path, data)
            if count == 2:
                raise OSError('écriture simulée')

        with self.assertRaises(OSError):
            self.m.apply_local(plans, self.remote, self.base / 'backup', writer=failing)
        self.assertEqual((target / 'SKILL.md').read_bytes(), b'ancien contenu\n')
        self.assertEqual((target / self.m.RECEIPT).read_bytes(), old_receipt)
        self.assertFalse((target / 'scripts/update.py').exists())

    def test_concurrent_edit_after_plan_is_preserved(self):
        target = self.local(tracked=True)
        plans = self.m.local_plan(self.remote, [('skills', self.skills)], False)
        (target / 'SKILL.md').write_bytes('édition concurrente'.encode())
        with self.assertRaisesRegex(self.m.UpdateError, 'concurrente'):
            self.m.apply_local(plans, self.remote, self.base / 'backup')
        self.assertEqual((target / 'SKILL.md').read_bytes(), 'édition concurrente'.encode())

    def test_application_lock_prevents_second_writer(self):
        with self.m.application_lock(self.home):
            with self.assertRaises(self.m.UpdateError):
                with self.m.application_lock(self.home):
                    self.fail('verrou concurrent accordé')

    def test_invalid_snapshot_cases_are_rejected(self):
        cases = []
        bad = dict(self.files)
        bad['plugins/cm/.codex-plugin/plugin.json'] = b'{"name":"cm","version":"0.1.0","skills":"./skills/"}'
        cases.append(zip_bytes(bad))
        bad = dict(self.files)
        bad['skills/tcu/scripts/update.py'] = b'def bad(\n'
        cases.append(zip_bytes(bad))
        cases.append(zip_bytes(self.files, ('snapshot/../escape.py', b'print(1)')))
        link = zipfile.ZipInfo('snapshot/skills/cm/linked.py')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        cases.append(zip_bytes(self.files, (link, b'/elsewhere')))
        cases.append(b'not a zip')
        for raw in cases:
            with self.subTest(raw=raw[:12]):
                def fetch(url):
                    return json.dumps({'sha': 'a' * 40}).encode() if url.endswith('/commits/HEAD') else raw
                with self.assertRaises(self.m.UpdateError):
                    self.m.snapshot(fetch)

    def test_http_and_network_failures_are_sanitized(self):
        http = HTTPError('https://api.github.com', 403, 'private fixture body', {}, io.BytesIO())
        for error in (http, URLError('private fixture endpoint')):
            opener = unittest.mock.Mock()
            opener.open.side_effect = error
            with patch.object(self.m, 'build_opener', return_value=opener):
                with self.assertRaises(self.m.UpdateError) as caught:
                    self.m.fetch('https://api.github.com/repos/' + self.m.REPOSITORY)
            self.assertNotIn('private fixture', str(caught.exception))
        self.assertFalse(self.m.allowed_url('http://api.github.com/'))
        self.assertFalse(self.m.allowed_url('https://github.com/'))

    def test_json_and_plugin_identity_errors_are_rejected(self):
        for raw in ('[]', '{', '{"x":NaN}', '{"x":1,"x":2}'):
            with self.assertRaises(self.m.UpdateError):
                self.m.decode_json(raw)
        entry = self.plugin()
        entry['marketplaceSource']['source'] = 'https://example.invalid/other.git'
        with self.assertRaises(self.m.UpdateError):
            self.m.installed(lambda _: {'installed': [entry]})

    def test_cli_error_does_not_echo_output(self):
        class Result:
            returncode = 1
            stdout = 'private fixture'
            stderr = 'private fixture'
        with patch.object(self.m.subprocess, 'run', return_value=Result()):
            with self.assertRaises(self.m.UpdateError) as caught:
                self.m.codex(['list', '--json'])
        self.assertNotIn('private fixture', str(caught.exception))

    def test_main_modes_and_failure_exit_code(self):
        for flags, expected in [([], False), (['check'], False), (['check', '--check'], False),
                                (['--check'], False), (['--apply'], True)]:
            with self.subTest(flags=flags):
                with patch.object(self.m, 'execute', return_value={'succes': True}) as execute:
                    with patch.dict(self.m.os.environ, {'CODEX_HOME': str(self.home)}):
                        with patch('sys.stdout', new_callable=io.StringIO):
                            self.assertEqual(self.m.main(flags + ['--skills-dir', str(self.skills)]), 0)
                self.assertEqual(execute.call_args.args[2], expected)
                self.assertEqual(execute.call_args.args[3], False)
        with patch.object(self.m, 'execute', side_effect=self.m.UpdateError('conflit détecté')):
            with patch('sys.stdout', new_callable=io.StringIO) as output:
                self.assertEqual(self.m.main(['--check']), 1)
        self.assertFalse(json.loads(output.getvalue())['succes'])

    def test_plain_check_rejects_apply_before_engine_execution(self):
        with patch.object(self.m, 'execute') as execute:
            with patch('sys.stderr', new_callable=io.StringIO):
                with self.assertRaises(SystemExit) as caught:
                    self.m.main(['check', '--apply'])
        self.assertEqual(caught.exception.code, 2)
        execute.assert_not_called()

    def test_bad_receipt_and_version_downgrade_preserve_sources(self):
        target = self.local(tracked=True)
        path = target / self.m.RECEIPT
        original = path.read_bytes()
        for data in (b'{', original.replace(b'0.2.3', b'9.0.0')):
            with self.subTest(data=data[:8]):
                self.upgraded = False
                path.write_bytes(data)
                report = self.execute(apply=True, adopt=True)
                self.assertFalse(report['succes'])
                self.assertTrue(self.upgraded)
                self.assertEqual((target / 'SKILL.md').read_bytes(), b'ancien contenu\n')

    def test_network_bounds_and_redirect_validation(self):
        with patch.object(self.m, 'LIMIT', 50):
            with self.assertRaises(self.m.UpdateError):
                self.m.snapshot(self.fetcher)
        for url in ('https://api.github.com:bad/', 'https://user:pass@api.github.com/', 'https://example.invalid/'):
            self.assertFalse(self.m.allowed_url(url))
        with self.assertRaises(self.m.UpdateError):
            self.m.SafeRedirect().redirect_request(None, None, 302, '', {}, 'https://example.invalid/')

    def test_plugin_build_metadata_keeps_the_same_release(self):
        self.before = {'cm': self.plugin()}
        self.after = {'cm': self.plugin('0.3.0+fixture')}
        self.cache('0.2.3')
        self.cache('0.3.0+fixture')
        result = self.execute(apply=True)
        self.assertTrue(result['succes'])
        self.assertEqual(next(r for r in result['briques'] if r['brique'] == 'cm')['apres'], '0.3.0+fixture')

    def test_prompt_check_plans_installation_without_any_write(self):
        self.enable_prompt()
        report = self.execute()
        self.assertTrue(report['succes'])
        self.assertFalse(self.home.exists())
        self.assertFalse(self.upgraded)
        self.assertFalse(any(c[0] == 'add' for c in self.calls))
        plugin = next(r for r in report['briques'] if r['brique'] == 'prompt')
        self.assertEqual(plugin['status'], 'a_installer')
        self.assertIsNone(plugin['apres'])
        command = next(r for r in report['briques'] if r.get('ressource') == 'commande')
        self.assertEqual(command['operation'], 'installer')
        self.assertIsNone(command['apres'])
        self.assertEqual(command['brique'], str(self.home / 'prompts/PROMPT.md'))

    def test_historical_command_names_keep_their_receipts_and_do_not_create_duplicates(self):
        commands = self.base / 'commands'
        commands.mkdir()
        hashes = {}
        for name in ('CM', 'PLLM', 'TFL'):
            rel = name.lower() + '.md'
            (commands / rel).write_bytes(b'tracked command')
            hashes[rel] = self.m.digest(b'tracked command')
            self.files['.codex/commands/' + name + '.md'] = name.encode() + b' canonical source'
        (commands / self.m.RECEIPT).write_text(json.dumps({
            'schema': 1, 'repository': self.m.REPOSITORY, 'sha': 'b' * 40,
            'version': '0.2.3', 'hashes': hashes}))
        report = self.execute(apply=True, roots=[('commands', commands)])
        self.assertTrue(report['succes'])
        for name in ('CM', 'PLLM', 'TFL'):
            rel = name.lower() + '.md'
            self.assertEqual((commands / rel).read_bytes(), name.encode() + b' canonical source')
            self.assertFalse((commands / (name + '.md')).exists())
        self.assertEqual(set(json.loads((commands / self.m.RECEIPT).read_text())['hashes']), set(hashes))
        self.assertFalse((commands / 'TCU.md').exists())

    def test_uppercase_command_source_keeps_legacy_local_edits_and_links(self):
        self.files['.codex/commands/CM.md'] = b'new canonical command'
        for linked in (False, True):
            with self.subTest(linked=linked):
                commands = self.base / ('linked' if linked else 'edited')
                commands.mkdir()
                path = commands / 'cm.md'
                if linked:
                    original = self.base / 'linked-command-source.md'
                    original.write_bytes(b'local command')
                    path.symlink_to(original)
                else:
                    path.write_bytes(b'local command')
                (commands / self.m.RECEIPT).write_text(json.dumps({
                    'schema': 1, 'repository': self.m.REPOSITORY, 'sha': 'b' * 40,
                    'version': '0.2.3', 'hashes': {'cm.md': self.m.digest(b'old command')}}))
                report = self.execute(apply=True, adopt=True, roots=[('commands', commands)])
                self.assertFalse(report['succes'])
                self.assertEqual(path.read_bytes(), b'local command')
                self.assertEqual(path.is_symlink(), linked)
                self.assertFalse((commands / 'CM.md').exists())

    def test_historical_prompt_receipt_updates_in_place_without_duplicate(self):
        self.enable_prompt()
        commands = self.home / 'prompts'
        commands.mkdir(parents=True)
        (commands / 'prompt.md').write_bytes(b'tracked legacy prompt')
        (commands / self.m.PROMPT_RECEIPT).write_text(json.dumps({
            'schema': 1, 'repository': self.m.REPOSITORY, 'sha': 'b' * 40,
            'version': '0.2.3', 'hashes': {'prompt.md': self.m.digest(b'tracked legacy prompt')}}))
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertEqual((commands / 'prompt.md').read_bytes(), self.files[self.m.PROMPT_COMMAND])
        self.assertFalse((commands / 'PROMPT.md').exists())
        self.assertEqual(set(json.loads((commands / self.m.PROMPT_RECEIPT).read_text())['hashes']), {'prompt.md'})
        self.assertTrue(any(p.read_bytes() == b'tracked legacy prompt'
                            for p in Path(report['backup']).rglob('prompt.md')))

    def test_both_prompt_names_are_verified_together(self):
        self.enable_prompt()
        commands = self.home / 'prompts'
        commands.mkdir(parents=True)
        for name in ('PROMPT.md', 'prompt.md'):
            (commands / name).write_bytes(b'tracked prompt')
        (commands / self.m.PROMPT_RECEIPT).write_text(json.dumps({
            'schema': 1, 'repository': self.m.REPOSITORY, 'sha': 'b' * 40,
            'version': '0.2.3', 'hashes': {name: self.m.digest(b'tracked prompt')
                                        for name in ('PROMPT.md', 'prompt.md')}}))
        self.assertTrue(self.execute(apply=True)['succes'])
        for name in ('PROMPT.md', 'prompt.md'):
            self.assertEqual((commands / name).read_bytes(), self.files[self.m.PROMPT_COMMAND])
        receipt = (commands / self.m.PROMPT_RECEIPT).read_bytes()
        (commands / 'prompt.md').write_bytes(b'local edit')
        report = self.execute(apply=True, adopt=True)
        self.assertFalse(report['succes'])
        self.assertEqual((commands / 'prompt.md').read_bytes(), b'local edit')
        self.assertEqual((commands / self.m.PROMPT_RECEIPT).read_bytes(), receipt)

    def test_previous_release_with_lowercase_prompt_source_is_still_readable(self):
        self.enable_prompt()
        self.files['.codex/commands/prompt.md'] = self.files.pop(self.m.PROMPT_COMMAND)
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertEqual((self.home / 'prompts/PROMPT.md').read_bytes(),
                         self.files['.codex/commands/prompt.md'])

    def test_prompt_installation_manages_plugin_skill_and_command_only(self):
        self.enable_prompt()
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertEqual([c for c in self.calls if c[0] == 'add'], [['add', 'prompt@tools-codex', '--json']])
        command = self.home / 'prompts/PROMPT.md'
        self.assertEqual(command.read_bytes(), self.files[self.m.PROMPT_COMMAND])
        receipt = json.loads((command.parent / self.m.PROMPT_RECEIPT).read_text())
        self.assertEqual(set(receipt['hashes']), {'PROMPT.md'})
        self.assertFalse((command.parent / self.m.RECEIPT).exists())
        self.assertFalse((self.skills / 'prompt').exists())
        rows = [r for r in report['briques'] if r['brique'] in {'prompt', 'prompt/skill'}]
        self.assertTrue(all(r['apres'] == '0.3.0' and r['status'] == 'installe' for r in rows))
        self.assertTrue(all(r['status'] == 'absent' for r in report['briques'] if r['canal'] == 'marketplace' and r['brique'] in {'cm', 'tcu'}))

    def test_prompt_existing_plugin_and_wrapper_update_without_reinstall(self):
        self.enable_prompt()
        self.assertTrue(self.execute(apply=True)['succes'])
        self.before = copy.deepcopy(self.after)
        self.upgraded = False
        self.calls.clear()
        self.source_sha = 'c' * 40
        original = self.files[self.m.PROMPT_COMMAND]
        self.files[self.m.PROMPT_COMMAND] = b'Nouvelle commande prompt\n'
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertFalse(any(c[0] == 'add' for c in self.calls))
        self.assertEqual((self.home / 'prompts/PROMPT.md').read_bytes(), b'Nouvelle commande prompt\n')
        self.assertTrue(any(p.read_bytes() == original for p in Path(report['backup']).rglob('PROMPT.md')))
        command = next(r for r in report['briques'] if r.get('ressource') == 'commande')
        self.assertEqual(command['status'], 'mis_a_jour')

    def test_link_conflict_does_not_block_plugin_command_or_other_data(self):
        self.enable_prompt()
        commands = self.base / 'commands'
        commands.mkdir()
        original = self.base / 'development-command.md'
        original.write_bytes(b'development source')
        linked = commands / 'TCU.md'
        linked.symlink_to(original)
        self.before = {'cm': self.plugin()}
        self.after = {'cm': self.plugin('0.3.0')}
        self.cache('0.2.3', b'preserved quotas')
        updated = self.cache('0.3.0', b'sample')
        report = self.execute(apply=True, roots=[('commands', commands)])
        self.assertFalse(report['succes'])
        self.assertTrue(linked.is_symlink())
        self.assertEqual(original.read_bytes(), b'development source')
        self.assertEqual((commands / 'PROMPT.md').read_bytes(), self.files[self.m.PROMPT_COMMAND])
        self.assertEqual((updated / 'skills/cm/data/report.json').read_bytes(), b'preserved quotas')
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'cm')['apres'], '0.3.0')
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'prompt')['apres'], '0.3.0')
        self.assertTrue(any(r['status'] == 'conflit' for r in report['briques']))

    def test_prompt_target_link_is_preserved_even_with_adoption(self):
        self.enable_prompt()
        commands = self.base / 'commands'
        commands.mkdir()
        source = self.base / 'original.md'
        source.write_bytes(b'unchanged linked source')
        path = commands / 'prompt.md'
        path.symlink_to(source)
        report = self.execute(apply=True, adopt=True, roots=[('commands', commands)])
        self.assertFalse(report['succes'])
        self.assertTrue(path.is_symlink())
        self.assertEqual(source.read_bytes(), b'unchanged linked source')
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'prompt')['status'], 'installe')

    def test_prompt_unknown_wrapper_requires_adoption_but_not_for_plugin(self):
        self.enable_prompt()
        commands = self.base / 'commands'
        commands.mkdir()
        (commands / 'prompt.md').write_bytes(b'old untracked wrapper')
        report = self.execute(apply=True, roots=[('commands', commands)])
        self.assertFalse(report['succes'])
        self.assertEqual((commands / 'prompt.md').read_bytes(), b'old untracked wrapper')
        self.assertIn('prompt', self.after)
        report = self.execute(apply=True, adopt=True, roots=[('commands', commands)])
        self.assertTrue(report['succes'])
        self.assertEqual((commands / 'prompt.md').read_bytes(), self.files[self.m.PROMPT_COMMAND])
        self.assertTrue(any(p.read_bytes() == b'old untracked wrapper' for p in Path(report['backup']).rglob('prompt.md')))

    def test_legacy_command_receipt_transfers_prompt_provenance_without_overwriting(self):
        self.enable_prompt()
        commands = self.base / 'commands'
        commands.mkdir()
        (commands / 'prompt.md').write_bytes(b'tracked old wrapper')
        (commands / 'other.md').write_bytes(b'other command')
        receipt = json.dumps({'schema': 1, 'repository': self.m.REPOSITORY, 'sha': 'b' * 40,
                              'version': '0.2.3', 'hashes': {'prompt.md': self.m.digest(b'tracked old wrapper'),
                                                          'other.md': self.m.digest(b'other command')}}).encode()
        (commands / self.m.RECEIPT).write_bytes(receipt)
        report = self.execute(apply=True, roots=[('commands', commands)])
        self.assertTrue(report['succes'])
        self.assertEqual((commands / self.m.RECEIPT).read_bytes(), receipt)
        self.assertEqual((commands / 'other.md').read_bytes(), b'other command')
        self.assertEqual(set(json.loads((commands / self.m.PROMPT_RECEIPT).read_text())['hashes']), {'prompt.md'})

    def test_prompt_tracked_wrapper_changes_are_not_forced(self):
        self.enable_prompt()
        self.assertTrue(self.execute(apply=True)['succes'])
        path = self.home / 'prompts/PROMPT.md'
        path.write_bytes(b'local edit')
        report = self.execute(apply=True, adopt=True)
        self.assertFalse(report['succes'])
        self.assertEqual(path.read_bytes(), b'local edit')

    def test_prompt_incomplete_source_blocks_every_mutation(self):
        self.enable_prompt()
        for key in [self.m.PROMPT_COMMAND, self.m.PROMPT_RESOLVER]:
            original = self.files.pop(key)
            with self.subTest(key=key):
                with self.assertRaises(self.m.UpdateError):
                    self.execute(apply=True)
                self.assertFalse(self.calls)
                self.assertFalse(self.home.exists())
            self.files[key] = original

    def test_command_sources_are_publishable_without_local_codex_files(self):
        commands = ['.codex/commands/' + name for name in
                    ('CM.md', 'PLLM.md', 'TFL.md', 'TCU.md', 'LM.md', 'PROMPT.md')]
        local_files = ['.codex/config.toml', '.codex/private-local.txt',
                       '.codex/state/runtime.json']
        for path in commands:
            self.assertTrue((ROOT / path).is_file(), path)
        result = subprocess.run(
            ['git', '-c', 'safe.directory=' + str(ROOT), '-C', str(ROOT),
             'check-ignore', '--no-index', '--stdin'],
            input='\n'.join(commands + local_files) + '\n',
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), local_files)

    def test_prompt_incomplete_cache_is_repaired_through_cli(self):
        self.enable_prompt()
        self.before = {'prompt': self.prompt_entry(enabled=False)}
        self.prompt_cache('0.3.0', complete=False)
        report = self.execute(apply=True)
        self.assertTrue(report['succes'])
        self.assertFalse(self.after['prompt']['enabled'])
        self.assertTrue(any(c[0] == 'add' for c in self.calls))
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'prompt/skill')['apres'], '0.3.0')

    def test_prompt_corrupt_cache_is_reported_and_wrapper_not_written(self):
        self.enable_prompt()
        original = self.prompt_cache

        def corrupt(release, complete=True):
            package = original(release, complete)
            (package / self.m.PROMPT_RESOLVER).write_bytes(b'print("wrong bytes")\n')
            return package

        with patch.object(self, 'prompt_cache', side_effect=corrupt):
            report = self.execute(apply=True)
        self.assertFalse(report['succes'])
        self.assertFalse((self.home / 'prompts/PROMPT.md').exists())
        skill = next(r for r in report['briques'] if r['brique'] == 'prompt/skill')
        self.assertEqual(skill['status'], 'incomplet')
        self.assertIsNone(skill['apres'])

    def test_prompt_install_failure_keeps_observed_effect_and_stops_wrapper(self):
        self.enable_prompt()
        original = self.runner

        def failing(args):
            value = original(args)
            if args[0] == 'add':
                raise self.m.UpdateError('échec après installation simulée')
            return value

        with patch.object(self, 'runner', side_effect=failing):
            report = self.execute(apply=True)
        self.assertFalse(report['succes'])
        self.assertFalse((self.home / 'prompts/PROMPT.md').exists())
        self.assertEqual(next(r for r in report['briques'] if r['brique'] == 'prompt')['apres'], '0.3.0')
        self.assertIn('échec', report['erreur'])

    def test_prompt_explicit_command_root_and_existing_autonomous_copy(self):
        self.enable_prompt()
        local = self.local('prompt', tracked=True)
        commands = self.base / 'new command root'
        report = self.execute(apply=True, roots=[('skills', self.skills), ('commands', commands)])
        self.assertTrue(report['succes'])
        self.assertEqual((commands / 'PROMPT.md').read_bytes(), self.files[self.m.PROMPT_COMMAND])
        self.assertFalse((self.home / 'prompts').exists())
        self.assertEqual((local / 'SKILL.md').read_bytes(), self.files[self.m.PROMPT_SKILL])
        self.assertEqual((local / 'scripts/resolve_prompt.py').read_bytes(), self.files[self.m.PROMPT_RESOLVER])


if __name__ == '__main__':
    unittest.main()
