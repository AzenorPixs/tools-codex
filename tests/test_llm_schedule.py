"""Planning isolé : aucun timer utilisateur ni appel fournisseur réel."""

from contextlib import ExitStack
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/tcu/scripts/scheduler.py'


def load(path=SOURCE):
    spec = importlib.util.spec_from_file_location('schedule_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def limits(used=25, secondary=50):
    return {'rateLimitsByLimitId': {'codex': {'limitId': 'codex',
            'primary': {'usedPercent': used}, 'secondary': {'usedPercent': secondary}}}}


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='schedule-', dir=ROOT / 'tests')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name) / 'profil avec espaces'
        self.home = self.base / 'codex'
        self.config = self.base / 'xdg'
        self.roots = self.base / 'skills'
        self.m = load()
        self.calls = []
        self.bad = None
        self.enabled = False
        self.active = False
        self.fake_codex = self.base / 'bin/codex'
        self.fake_codex.parent.mkdir(parents=True)
        self.fake_codex.write_text('#!/bin/sh\nexit 1\n')
        self.fake_codex.chmod(0o700)
        for name, filename in self.m.FILES.items():
            scripts = self.roots / name / 'scripts'
            scripts.mkdir(parents=True)
            for item in (filename, 'performance.py', 'model_blacklist.py', 'model_evidence.py'):
                (scripts / item).write_text('# fixture hors ligne\n')
        context = patch.object(self.m, 'development', return_value=False)
        context.start()
        self.addCleanup(context.stop)

    def runner(self, arguments, **kwargs):
        self.calls.append((arguments, kwargs))
        code = 0
        if arguments[1:3] == ['plugin', 'list']:
            return SimpleNamespace(returncode=0, stdout=json.dumps({'installed': []}))
        if arguments[:2] == ['systemctl', '--user']:
            action = arguments[2]
            if action == 'is-enabled':
                code = 0 if self.enabled else 1
            elif action == 'is-active':
                code = 0 if self.active else 1
            elif action == 'enable':
                self.enabled = self.active = True
            elif action == 'disable':
                self.enabled = self.active = False
            if action == self.bad:
                code = 1
        elif 'test_fournisseur_llm.py' in str(arguments):
            if self.bad != 'stale':
                destination = Path(arguments[arguments.index('--output-dir') + 1]) / 'tfl.json'
                destination.parent.mkdir(parents=True, exist_ok=True)
                data = {name: {'models': [{'id': 'fixture'}]} for name in ('opencode_go', 'opencode', 'openrouter')}
                destination.write_text(json.dumps(data))
            code = 1 if self.bad == 'tfl' else 0
        elif 'evaluate.py' in str(arguments):
            code = 1 if self.bad == 'pllm' else 0
        return SimpleNamespace(returncode=code, stdout='')

    def install(self, apply=True):
        return self.m.install(self.home, [self.roots], self.config, apply, self.runner, codex=self.fake_codex)

    def evaluate(self, quotas=('available', 'available'), active=True):
        self.calls.clear()
        self.events = []
        readings = iter(quotas)
        def quota(*args):
            self.events.append('quota')
            return next(readings)
        def run(args, **kwargs):
            self.events.append('tfl' if 'test_fournisseur_llm.py' in str(args) else 'pllm')
            return self.runner(args, **kwargs)
        return self.m.run_refresh(self.home, self.config, run, quota, lambda: active)

    def test_install_check_idempotence_and_paris_timer(self):
        self.assertEqual(self.install(False)['status'], 'a_installer')
        self.assertFalse(self.home.exists())
        self.assertFalse(self.config.exists())
        self.assertEqual(self.calls, [])
        self.assertEqual(self.install()['status'], 'installe')
        paths = self.m.layout(self.home, self.config)[1]
        previous = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
        self.calls.clear()
        self.assertEqual(self.install()['status'], 'courant')
        self.assertEqual(previous, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths})
        self.assertFalse(any(args[2] in ('enable', 'daemon-reload') for args, _ in self.calls))
        timer = paths[-1].read_text()
        self.assertIn('OnCalendar=*-*-* 00,12:00:00 Europe/Paris', timer)
        self.assertIn('Persistent=false', timer)
        self.assertIn('DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/', paths[-2].read_text())
        self.assertEqual(paths[0].read_bytes(), SOURCE.read_bytes())

    def test_components_missing_do_not_install_or_generate(self):
        shutil.rmtree(self.roots / 'pllm')
        self.assertEqual(self.install()['status'], 'composants_absents')
        self.assertFalse(self.home.exists())
        self.assertFalse(self.config.exists())
        self.assertFalse(any('evaluate.py' in str(call) for call in self.calls))

    def test_managed_update_preserves_foreign_units_and_reports(self):
        self.install()
        foreign = self.config / 'systemd/user/other.timer'
        foreign.write_text('ne pas toucher\n')
        report = self.roots / 'pllm/data/pllm-current.json'
        report.parent.mkdir()
        report.write_text('historique conservé')
        changed = self.base / 'new-scheduler.py'
        changed.write_bytes(SOURCE.read_bytes() + b'\n# fixture de version suivante\n')
        result = self.m.install(self.home, [self.roots], self.config, runner=self.runner,
                               source=changed, codex=self.fake_codex)
        self.assertEqual(result['status'], 'mis_a_jour')
        self.assertEqual(foreign.read_text(), 'ne pas toucher\n')
        self.assertEqual(report.read_text(), 'historique conservé')
        self.assertEqual(self.m.remove(self.home, self.config, self.runner)['status'], 'retire')
        self.assertTrue(foreign.exists())
        self.assertTrue(report.exists())
        self.assertEqual(self.m.remove(self.home, self.config, self.runner)['status'], 'absent')

    def test_foreign_and_modified_files_are_not_overwritten_or_removed(self):
        unit = self.config / 'systemd/user' / (self.m.UNIT + '.timer')
        unit.parent.mkdir(parents=True)
        unit.write_text('étranger')
        with self.assertRaises(self.m.ScheduleError):
            self.install()
        self.assertEqual(unit.read_text(), 'étranger')
        unit.unlink()
        self.install()
        unit.write_text('modification utilisateur')
        for operation in (self.install, lambda: self.m.remove(self.home, self.config, self.runner)):
            with self.assertRaises(self.m.ScheduleError):
                operation()
        self.assertEqual(unit.read_text(), 'modification utilisateur')

    def test_link_paths_and_other_owners_are_refused(self):
        target = self.base / 'target'
        target.mkdir()
        self.home.symlink_to(target)
        with self.assertRaises(self.m.ScheduleError):
            self.install()
        self.assertEqual(list(target.iterdir()), [])
        current_uid = os.getuid()
        with patch.object(self.m.os, 'getuid', return_value=current_uid + 1):
            with self.assertRaises(self.m.ScheduleError):
                self.m.safe(target)

    def test_activity_does_not_use_another_user(self):
        proc = self.base / 'proc'
        entry = proc / '123'
        (entry / 'fd').mkdir(parents=True)
        (entry / 'exe').symlink_to('/opt/Codex/codex')
        (entry / 'stat').write_text('123 (codex) S 1 0 0\n')
        (entry / 'cmdline').write_bytes(b'codex\x00')
        (entry / 'fd/0').symlink_to('/dev/null')
        self.assertTrue(self.m.codex_active(proc))
        self.assertFalse(self.m.codex_active(proc, uid=os.getuid() + 1))

    def test_unified_frontend_requires_its_own_live_codex_backend(self):
        proc = self.base / 'proc'
        for pid, parent, exe, args in ((123, 1, '/usr/lib/chatgpt/chatgpt', b'chatgpt\x00'),
                                      (124, 123, '/usr/lib/chatgpt/resources/codex', b'codex\x00app-server\x00')):
            entry = proc / str(pid)
            (entry / 'fd').mkdir(parents=True)
            (entry / 'exe').symlink_to(exe)
            (entry / 'stat').write_text(str(pid) + ' (fixture) S ' + str(parent) + ' 0 0\n')
            (entry / 'cmdline').write_bytes(args)
        self.assertTrue(self.m.codex_active(proc))
        (proc / '124/stat').write_text('124 (fixture) S 1 0 0\n')
        self.assertFalse(self.m.codex_active(proc))
        shutil.rmtree(proc / '124')
        self.assertFalse(self.m.codex_active(proc))

    def test_failed_activation_restores_previous_files(self):
        self.bad = 'enable'
        with self.assertRaises(self.m.ScheduleError):
            self.install()
        self.assertTrue(all(not p.exists() for p in self.m.layout(self.home, self.config)[1]))
        self.bad = None
        self.install()
        paths = self.m.layout(self.home, self.config)[1]
        saved = {p: p.read_bytes() for p in paths}
        replacement = self.base / 'changed.py'
        replacement.write_bytes(SOURCE.read_bytes() + b'\n# fixture\n')
        self.bad = 'daemon-reload'
        with self.assertRaises(self.m.ScheduleError):
            self.m.install(self.home, [self.roots], self.config, runner=self.runner,
                           source=replacement, codex=self.fake_codex)
        self.assertEqual(saved, {p: p.read_bytes() for p in paths})

    def test_application_and_interactive_cli_only(self):
        cases = [('/opt/Codex/codex', ['codex'], '', True),
                 ('/usr/bin/codex', ['codex'], '/dev/pts/4', True),
                 ('/usr/bin/codex', ['codex', 'resume'], '/dev/pts/4', True),
                 ('/usr/bin/codex', ['codex', 'app-server'], '/dev/pts/4', False),
                 ('/opt/Codex/codex', ['codex', '--type=renderer'], '', False),
                 ('/usr/bin/codex', ['codex', 'exec'], '/dev/pts/4', False),
                 ('/usr/bin/codex', ['codex'], '', False),
                 ('/usr/bin/python3', ['python3', 'codex'], '/dev/pts/4', False)]
        for exe, args, terminal, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(self.m.process_active(exe, args, terminal), expected)

    def test_no_active_codex_skips_quota_and_all_generations(self):
        self.install()
        self.assertEqual(self.evaluate(quotas=(), active=False)['status'], 'ignore_codex_ferme')
        self.assertEqual(self.events, [])
        self.assertEqual(self.calls, [])

    def test_codex_quota_normalization_prefers_codex_not_spark(self):
        self.assertEqual(self.m.quota_state(limits()), 'available')
        for data in (limits(100), limits(15, 100), limits(120)):
            self.assertEqual(self.m.quota_state(data), 'exhausted')
        data = limits()
        data['rateLimitsByLimitId']['spark'] = {'limitId': 'spark', 'primary': {'usedPercent': 100}}
        data['rateLimits'] = {'limitId': 'codex', 'primary': {'usedPercent': 100}}
        self.assertEqual(self.m.quota_state(data), 'available')
        self.assertEqual(self.m.quota_state({'rateLimits': {'limitId': 'codex', 'primary': {'usedPercent': 1}}}), 'available')
        for data in ({}, {'rateLimitsByLimitId': {'spark': {}}}, limits(None), limits(True),
                     limits(float('nan')), limits(float('inf')), limits(-1)):
            self.assertEqual(self.m.quota_state(data), 'unknown')

    def test_zero_or_unknown_quota_never_calls_tfl_or_pllm(self):
        self.install()
        for quota, status in (('exhausted', 'ignore_quota_epuise'), ('unknown', 'ignore_quota_inconnu')):
            with self.subTest(quota=quota):
                result = self.evaluate((quota,))
                self.assertEqual(result['status'], status)
                self.assertEqual(result['etape'], 'tfl')
                self.assertEqual(self.events, ['quota'])
                self.assertEqual(self.calls, [])

    def test_quota_is_rechecked_between_tfl_and_pllm(self):
        self.install()
        for quota, status in (('exhausted', 'ignore_quota_epuise'), ('unknown', 'ignore_quota_inconnu')):
            result = self.evaluate(('available', quota))
            self.assertEqual(result['status'], status)
            self.assertEqual(result['etape'], 'pllm')
            self.assertEqual(self.events, ['quota', 'tfl', 'quota'])

    def test_codex_closed_after_tfl_does_not_start_pllm(self):
        self.install()
        activities = iter((True, False))
        calls = []
        def quota(*args):
            calls.append('quota')
            return 'available'
        result = self.m.run_refresh(self.home, self.config, self.runner, quota, lambda: next(activities))
        self.assertEqual(result['status'], 'ignore_codex_ferme')
        self.assertEqual(result['etape'], 'pllm')
        self.assertEqual(calls, ['quota'])

    def test_tfl_timeout_is_recorded_without_raw_diagnostics(self):
        self.install()
        def failed(args, **kwargs):
            raise self.m.ScheduleError('fixture privée non publiée')
        result = self.m.run_refresh(self.home, self.config, failed, lambda *args: 'available', lambda: True)
        self.assertEqual(result['status'], 'echec_tfl')
        self.assertNotIn('privée', json.dumps(result))
        self.assertEqual(json.loads((self.home / 'llm-refresh/state.json').read_text()), result)

    def test_success_uses_fresh_explicit_catalog_and_normal_six_mode_command(self):
        self.install()
        self.assertEqual(self.evaluate()['status'], 'succes')
        self.assertEqual(self.events, ['quota', 'tfl', 'quota', 'pllm'])
        arguments, _ = self.calls[-1]
        self.assertNotIn('active', arguments)
        self.assertEqual(arguments[-2:], ['--tfl-catalog', str(self.roots / 'tfl/data/tfl.json')])
        state = json.loads((self.home / 'llm-refresh/state.json').read_text())
        self.assertEqual(state['status'], 'succes')

    def test_failure_stale_catalog_and_failed_pllm_are_distinct(self):
        self.install()
        self.bad = 'tfl'
        self.assertEqual(self.evaluate()['status'], 'echec_tfl')
        self.assertEqual(self.events, ['quota', 'tfl'])
        self.bad = 'stale'
        self.assertEqual(self.evaluate()['status'], 'catalogue_non_actualise')
        self.assertEqual(self.events, ['quota', 'tfl'])
        self.bad = 'pllm'
        self.assertEqual(self.evaluate()['status'], 'echec_pllm')

    def test_locks_prevent_duplicate_and_tcu_overlap(self):
        self.install()
        for path in (self.home / 'llm-refresh/operation.lock', self.home / 'tcu.lock'):
            with self.m.lock(path):
                self.assertEqual(self.evaluate(quotas=())['status'], 'ignore_occupe')
                self.assertEqual(self.events, [])

    def test_concurrent_hook_is_silent_and_does_not_block_codex(self):
        with patch.object(self.m, 'install', side_effect=self.m.ScheduleError('Opération déjà en cours')):
            with patch('sys.stdout', new_callable=io.StringIO) as output, patch('sys.stderr', new_callable=io.StringIO) as error:
                self.assertEqual(self.m.main(['install', '--hook']), 0)
        self.assertEqual(output.getvalue(), '')
        self.assertEqual(error.getvalue(), '')

    def test_plugin_resolution_follows_enabled_cli_version(self):
        shutil.rmtree(self.roots)
        entries = []
        for name, filename in self.m.FILES.items():
            scripts = self.home / 'plugins/cache/tools-codex' / name / '0.7.8/skills' / name / 'scripts'
            scripts.mkdir(parents=True)
            for item in (filename, 'performance.py', 'model_blacklist.py', 'model_evidence.py'):
                (scripts / item).write_text('# fixture\n')
            entries.append({'name': name, 'installed': True, 'enabled': True, 'marketplaceName': 'tools-codex',
                            'pluginId': name + '@tools-codex', 'version': '0.7.8'})
        def run(args, **kwargs):
            return SimpleNamespace(returncode=0, stdout=json.dumps({'installed': entries}))
        found = self.m.discover(self.home, [], run, self.fake_codex)
        self.assertEqual(set(found), {'tfl', 'pllm'})
        self.assertTrue(all('/0.7.8/' in str(path) for path in found.values()))
        entries[0]['enabled'] = False
        self.assertNotIn('tfl', self.m.discover(self.home, [], run, self.fake_codex))

    def test_rpc_only_initializes_and_reads_limits_without_exposing_other_fields(self):
        fake = self.base / 'rpc.py'
        recorded = self.base / 'methods.json'
        fake.write_text("import json,sys\nmethods=[]\nfor line in sys.stdin:\n"
                        " data=json.loads(line);methods.append(data['method'])\n"
                        " if data.get('id')==1: print(json.dumps({'id':1,'result':{}}),flush=True)\n"
                        " if data.get('id')==2:\n"
                        "  print(json.dumps({'id':2,'result':" + repr(limits()) + "}),flush=True)\n"
                        "  open(" + repr(str(recorded)) + ",'w').write(json.dumps(methods))\n  break\n")
        def popen(args, **kwargs):
            self.assertIn('--stdio', args)
            return subprocess.Popen([sys.executable, '-u', str(fake)], **kwargs)
        self.assertEqual(self.m.read_codex_quota(self.fake_codex, self.home, popen=popen), 'available')
        self.assertEqual(json.loads(recorded.read_text()), ['initialize', 'initialized', 'account/rateLimits/read'])

    def test_rpc_timeout_and_malformed_payload_are_unknown(self):
        fake = self.base / 'bad-rpc.py'
        fake.write_text("import sys\nfor line in sys.stdin:\n print('invalid-json',flush=True)\n break\n")
        def popen(args, **kwargs):
            return subprocess.Popen([sys.executable, '-u', str(fake)], **kwargs)
        self.assertEqual(self.m.read_codex_quota(self.fake_codex, self.home, popen=popen), 'unknown')
        fake.write_text('import time\ntime.sleep(0.15)\n')
        self.assertEqual(self.m.read_codex_quota(self.fake_codex, self.home, timeout=0.01, popen=popen), 'unknown')

    def test_six_plugin_hooks_and_twelve_isolated_modules(self):
        contents = set()
        for name in ('cm', 'lm', 'pllm', 'prompt', 'tcu', 'tfl'):
            plugin = ROOT / 'plugins' / name
            manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
            self.assertEqual(manifest['hooks'], './hooks/hooks.json')
            hooks = json.loads((plugin / 'hooks/hooks.json').read_text())
            handler = hooks['hooks']['SessionStart'][0]['hooks'][0]
            arguments = shlex.split(handler['command'].replace('${PLUGIN_ROOT}', str(plugin)))
            self.assertEqual(arguments[-2:], ['install', '--hook'])
            self.assertEqual(Path(arguments[1]), plugin / 'skills' / name / 'scripts/scheduler.py')
            for index, base in enumerate((ROOT / 'skills' / name, plugin / 'skills' / name)):
                path = base / 'scripts/scheduler.py'
                contents.add(path.read_bytes())
                copied = self.base / 'isolated' / name / str(index) / 'scripts/scheduler.py'
                copied.parent.mkdir(parents=True)
                copied.write_bytes(path.read_bytes())
                module = load(copied)
                with patch.object(module, 'development', return_value=False):
                    self.assertEqual(module.install(self.home, [self.roots], self.config, apply=False,
                                                    runner=self.runner, codex=self.fake_codex)['status'], 'a_installer')
        self.assertEqual(len(contents), 1)
        self.assertFalse(self.home.exists())
        self.assertFalse(self.config.exists())

    def test_real_systemd_calendar_handles_both_daylight_changes(self):
        if not shutil.which('systemd-analyze'):
            self.skipTest('systemd-analyze indisponible')
        for base, expected in (('2026-10-24 23:30:00 Europe/Paris',
                                ('2026-10-24 22:00:00 UTC', '2026-10-25 11:00:00 UTC')),
                               ('2026-03-28 23:30:00 Europe/Paris',
                                ('2026-03-28 23:00:00 UTC', '2026-03-29 10:00:00 UTC'))):
            result = subprocess.run(['systemd-analyze', 'calendar', '--iterations=2', '--base-time=' + base,
                                     self.m.CALENDAR], capture_output=True, text=True,
                                    env=dict(os.environ, LC_ALL='C', TZ='UTC'), check=False)
            self.assertEqual(result.returncode, 0)
            for value in expected:
                self.assertIn(value, result.stdout)

    def test_real_systemd_unit_parser_accepts_installed_units(self):
        if not shutil.which('systemd-analyze'):
            self.skipTest('systemd-analyze indisponible')
        self.install()
        paths = self.m.layout(self.home, self.config)[1][-2:]
        result = subprocess.run(['systemd-analyze', '--user', 'verify', *(str(p) for p in paths)],
                                capture_output=True, text=True, env=dict(os.environ, LC_ALL='C'), check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
