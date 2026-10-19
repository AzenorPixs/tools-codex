"""Qualification hors ligne TCU : jamais de réseau ni de profil utilisateur réel."""

import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import stat
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
        if url.endswith('/commits/HEAD'):
            return json.dumps({'sha': 'a' * 40}).encode()
        self.assertTrue(url.endswith('/zipball/' + 'a' * 40))
        return zip_bytes(self.files)

    def runner(self, args):
        self.calls.append(args)
        if args[0] == 'marketplace':
            self.assertEqual(args, ['marketplace', 'upgrade', 'tools-codex', '--json'])
            self.upgraded = True
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
        self.assertFalse(self.upgraded)
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
        self.assertFalse(self.upgraded)
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
        self.assertTrue(all(r['status'] == 'absent' for r in result['briques']))
        self.assertFalse(any(c[0] == 'add' for c in self.calls))

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
                path.write_bytes(data)
                report = self.execute(apply=True, adopt=True)
                self.assertFalse(report['succes'])
                self.assertFalse(self.upgraded)
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


if __name__ == '__main__':
    unittest.main()
