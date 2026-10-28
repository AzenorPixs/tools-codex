"""Gestion LM et exclusion avant génération ; profils et fournisseurs isolés."""

from eur_fixtures import FX

from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import test_extension_qualification as qualification
from test_extension_qualification import load_script, ROOT, PLLM, TFL
from test_pllm_free_fallback import row


HELPERS = tuple(ROOT / path / 'scripts/model_blacklist.py' for path in (
    'skills/lm', 'plugins/lm/skills/lm', 'skills/tfl', 'plugins/tfl/skills/tfl',
    'skills/pllm', 'plugins/pllm/skills/pllm'))


class LmBlacklistTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='lm-', dir=ROOT / 'tests')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.home = self.base / 'codex profile'
        environment = patch.dict(os.environ, {'CODEX_HOME': str(self.home)})
        environment.start()
        self.addCleanup(environment.stop)
        self.m = load_script(HELPERS[0])
        self.path = self.m.policy_path()

    def write(self, value):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(value, encoding='utf-8')

    def catalog(self):
        path = self.base / 'catalog.json'
        data = {'generated_at': 'fixture',
                'opencode_go': {'models': [row('mimo-v2.5'), row('allowed'),
                                            row('mimo-v2.5-free', free=True), row('allowed-free', free=True)]},
                'opencode': {'models': [row('vendor/mimo-v2.5:free', 'opencode', True),
                                        row('general-free', 'opencode', True)]},
                'openrouter': {'models': [row('xiaomi/mimo-v2.5', 'openrouter'),
                                          row('router-allowed', 'openrouter'),
                                          row('router-free', 'openrouter', True)]}}
        path.write_text(json.dumps(data), encoding='utf-8')
        return path

    def openrouter_live(self, rows):
        return {'data': [{'id': item['id'], 'name': item['id'], 'context_length': 1_000_000,
                          'pricing': {'prompt': str(item['input_price'] / 1_000_000),
                                      'completion': str(item['output_price'] / 1_000_000)}}
                         for item in rows]}

    def test_missing_policy_applies_default_without_writing(self):
        for helper in HELPERS:
            module = load_script(helper)
            self.assertEqual(module.load_models(), ('mimo-v2.5', 'muse-spark-1.2-contributor'))
            self.assertTrue(module.is_blocked('xiaomi/mimo-v2.5:free'))
        self.assertFalse(self.home.exists())

    def test_canonical_identity_and_nearby_names(self):
        for identifier in ('mimo-v2.5', 'xiaomi/mimo-v2.5', 'MIMO-V2.5-FREE', 'vendor/mimo-v2.5:free'):
            self.assertTrue(self.m.is_blocked(identifier), identifier)
        for identifier in ('vendor/mimo-v2.5-free-free', 'vendor/model:extended', 'MIMO-V2.5'):
            canonical = self.m.canonical_id(identifier)
            self.assertEqual(self.m.canonical_id(canonical),canonical)
        for identifier in ('mimo-v2.50', 'mimo-v2.5-pro', 'other'):
            self.assertFalse(self.m.is_blocked(identifier), identifier)
        for identifier in ('', '../model', 'bad model', 'bad\nmodel', '$model', 'é', 'x' * 257):
            with self.assertRaises(self.m.BlacklistError):
                self.m.canonical_id(identifier)

    def test_add_remove_shared_and_empty_list_persist(self):
        first, second = (load_script(p) for p in HELPERS[:2])
        self.assertEqual(first.update_models('ADD', 'vendor/OTHER:free'), ('mimo-v2.5', 'muse-spark-1.2-contributor', 'other'))
        before = self.path.read_bytes(), self.path.stat().st_mtime_ns
        first.update_models('ADD', 'other')
        self.assertEqual((self.path.read_bytes(), self.path.stat().st_mtime_ns), before)
        self.assertEqual(second.load_models(), ('mimo-v2.5', 'muse-spark-1.2-contributor', 'other'))
        second.update_models('REMOVE', 'mimo-v2.5')
        self.assertFalse(first.is_blocked('xiaomi/mimo-v2.5:free'))
        first.update_models('REMOVE', 'other')
        first.update_models('REMOVE', 'muse-spark-1.2-contributor')
        self.assertEqual(second.load_models(), ())
        second.update_models('REMOVE', 'absent')
        self.assertEqual(second.load_models(), ())
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)

    def test_marked_provider_keeps_canonical_identity_in_all_packages(self):
        cases = {
            '~unbiased/pareto-latest': 'pareto-latest',
            '~XIAOMI/MIMO-V2.5:free': 'mimo-v2.5',
            '~vendor/model-free-free:free': 'model',
            '~vendor/nested/model:extended': 'model:extended',
        }
        for helper in HELPERS:
            module = load_script(helper)
            for identifier, expected in cases.items():
                with self.subTest(helper=helper, identifier=identifier):
                    self.assertEqual(module.canonical_id(identifier), expected)
                    self.assertEqual(module.canonical_id(expected), expected)
                    self.assertEqual(module.canonical_id(identifier[1:]), expected)
            self.assertTrue(module.is_blocked('~XIAOMI/MIMO-V2.5:free'))
            self.assertTrue(module.is_blocked('~meta/muse-spark-1.2-contributor-free'))
            for identifier in ('~xiaomi/mimo-v2.50', '~xiaomi/mimo-v2.5-pro'):
                self.assertFalse(module.is_blocked(identifier))

    def test_marked_provider_does_not_relax_grammar_or_full_length_limit(self):
        invalid = ('~model', '~~vendor/model', 'vendor/~model', '~vendor/~model',
                   '~vendor/', '~/model', '~vendor//model', '~../model',
                   '~vendor/model~', '~vendor/model:free:free', '~vendor/bad model',
                   '~vendor/model\n', '~vendor/\x00model', '~vendor/é',
                   '~v/' + 'x' * 254, None, 12)
        for helper in HELPERS:
            module = load_script(helper)
            boundary = '~v/' + 'x' * 253
            self.assertEqual(len(boundary), 256)
            self.assertEqual(module.canonical_id(boundary), 'x' * 253)
            for identifier in invalid:
                with self.subTest(helper=helper, identifier=identifier):
                    with self.assertRaises(module.BlacklistError):
                        module.canonical_id(identifier)
        self.assertFalse(self.home.exists())

    def test_marked_crud_uses_shared_identity_without_losing_exclusions(self):
        self.assertEqual(self.m.update_models('ADD', '~vendor/CUSTOM:free'),
                         ('custom', 'mimo-v2.5', 'muse-spark-1.2-contributor'))
        for helper in HELPERS:
            module = load_script(helper)
            for identifier in ('custom', 'vendor/custom', '~other/CUSTOM-free'):
                self.assertTrue(module.is_blocked(identifier))
            self.assertFalse(module.is_blocked('~vendor/custom-pro'))
            module.update_models('REMOVE', '~meta/muse-spark-1.2-contributor')
            self.assertFalse(module.is_blocked('~meta/muse-spark-1.2-contributor'))
        self.assertEqual(json.loads(self.path.read_text())['models'], ['custom', 'mimo-v2.5'])
        self.assertEqual(self.m.update_models('REMOVE', '~vendor/custom-free'), ('mimo-v2.5',))
        self.assertTrue(self.m.is_blocked('~xiaomi/mimo-v2.5'))

    def test_marked_duplicate_or_invalid_policy_stays_blocking_and_preserved(self):
        for models in (['model', '~vendor/MODEL:free'], ['~model'], ['vendor/~model']):
            raw = json.dumps({'schema_version': 1, 'models': models})
            self.write(raw)
            for helper in HELPERS:
                module = load_script(helper)
                with self.assertRaises(module.BlacklistError):
                    module.load_models()
                with self.assertRaises(module.BlacklistError):
                    module.update_models('ADD', 'other')
                self.assertEqual(self.path.read_text(), raw)

    def test_old_permanent_exclusion_is_removable_in_every_distribution(self):
        self.assertTrue(self.m.is_blocked('meta/muse-spark-1.2-contributor'))
        self.m.update_models('REMOVE', 'muse-spark-1.2-contributor')
        for helper in HELPERS:
            module = load_script(helper)
            self.assertFalse(module.is_blocked('~meta/muse-spark-1.2-contributor-free'))

    def test_explicit_empty_policy_has_no_residual_blacklist(self):
        self.write('{"schema_version":1,"models":[]}')
        for helper in HELPERS:
            module = load_script(helper)
            self.assertEqual(module.load_models(), ())
            self.assertFalse(module.is_blocked('muse-spark-1.2-contributor'))
            self.assertFalse(module.is_blocked('mimo-v2.5'))

    def test_corrupt_schema_or_duplicates_are_preserved(self):
        cases = ('{', '[]', '{"schema_version":2,"models":[]}',
                 '{"schema_version":true,"models":[]}',
                 '{"schema_version":1,"models":[],"models":[]}',
                 '{"schema_version":1,"models":["a","vendor/A"]}',
                 '{"schema_version":1,"models":[null]}',
                 '{"schema_version":1,"models":["bad model"]}',
                 '{"schema_version":1,"models":[],"other":NaN}')
        for raw in cases:
            with self.subTest(raw=raw):
                self.write(raw)
                for operation in (lambda: self.m.load_models(), lambda: self.m.update_models('ADD', 'other')):
                    with self.assertRaises(self.m.BlacklistError):
                        operation()
                self.assertEqual(self.path.read_text(), raw)

    def test_oversized_and_unreadable_policy_block(self):
        self.write(' ' * (self.m.MAX_BYTES + 1))
        with self.assertRaises(self.m.BlacklistError):
            self.m.load_models()
        with patch.object(Path, 'open', side_effect=PermissionError('private fixture')):
            with self.assertRaises(self.m.BlacklistError) as caught:
                self.m.load_models()
        self.assertNotIn('private fixture', str(caught.exception))

    def test_failed_atomic_replace_preserves_previous_content(self):
        self.m.update_models('ADD', 'first')
        before = self.path.read_bytes()
        with patch.object(self.m.os, 'replace', side_effect=OSError('private fixture')):
            with self.assertRaises(self.m.BlacklistError):
                self.m.update_models('ADD', 'second')
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.glob('.blacklist-*')), [])

    def test_concurrent_writer_cannot_lose_an_update(self):
        second = load_script(HELPERS[1])
        with self.m._writer_lock(self.path):
            with self.assertRaisesRegex(second.BlacklistError, 'déjà en cours'):
                second.update_models('ADD', 'other')
        self.m.update_models('ADD', 'after-lock')
        self.assertIn('after-lock', self.m.load_models())

    def test_file_symlink_is_never_overwritten(self):
        destination = self.base / 'other.json'
        destination.write_text('preserved')
        self.path.parent.mkdir(parents=True)
        self.path.symlink_to(destination)
        with self.assertRaises(self.m.BlacklistError):
            self.m.update_models('ADD', 'other')
        self.assertTrue(self.path.is_symlink())
        self.assertEqual(destination.read_text(), 'preserved')

    def test_cli_list_and_crud_in_both_isolated_packages(self):
        for index, source in enumerate((ROOT / 'skills/lm', ROOT / 'plugins/lm/skills/lm')):
            package = self.base / str(index) / 'lm'
            shutil.copytree(source, package)
            environment = dict(os.environ, CODEX_HOME=str(self.base / str(index) / 'profile'))
            script = package / 'scripts/lm.py'
            def run(*arguments):
                return subprocess.run([sys.executable, '-B', str(script), *arguments], env=environment,
                                      capture_output=True, text=True, check=False)
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('mimo-v2.5', result.stdout)
            self.assertFalse(Path(environment['CODEX_HOME']).exists())
            self.assertEqual(run('ADD', 'vendor/other:free').returncode, 0)
            self.assertIn('| other |', run('LIST').stdout)
            self.assertEqual(run('REMOVE', 'other').returncode, 0)
            self.assertNotIn('| other |', run('LIST').stdout)
            for arguments in (('ADD',), ('LIST', 'other'), ('REMOVE', 'bad model'), ('unknown',)):
                self.assertNotEqual(run(*arguments).returncode, 0)

    def test_tfl_all_three_catalogs_exclude_before_metadata_or_price(self):
        for script in TFL:
            module = load_script(script)
            for general in (False, True):
                payload = {'data': [{'id': 'vendor/mimo-v2.5:free'}]}
                rows, excluded = module.build_rows(payload, {'provider_id': 'opencode'} if general else {}, {}, general_catalog=general)
                self.assertEqual(rows, [])
                self.assertIn('LM', excluded[0]['reason'])
            rows, excluded = module.build_openrouter_rows({'data': [{'id': 'xiaomi/mimo-v2.5'},
                {'reasoning_capabilities': {'supported_efforts': ['medium']}, 'id':'allowed','context_length':1_000_000,'pricing':{'prompt':'0.0000001','completion':'0.0000001'}}]}, exchange_rates=FX)
            self.assertEqual([item['id'] for item in rows], ['allowed'])
            self.assertIn('LM', excluded[0]['reason'])

    def test_tfl_free_guard_never_reaches_generation(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                for identifier in ('mimo-v2.5', '~xiaomi/MIMO-V2.5:free'):
                    excluded, audit = [], []
                    with patch.object(module, 'evaluate_free') as evaluate:
                        self.assertEqual(module.qualify_free_models([row(identifier, section, True)], excluded, section, 'offline', audit), [])
                    evaluate.assert_not_called()
                    self.assertEqual(audit, [])
                    self.assertEqual(len(excluded), 1)
            for identifier in ('mimo-v2.5', '~xiaomi/MIMO-V2.5:free'):
                with patch.object(module.performance, 'run_benchmark') as benchmark:
                    with self.assertRaises(RuntimeError):
                        module.evaluate_free({'model_id': identifier}, 'offline', {})
                benchmark.assert_not_called()

    def test_tfl_full_collection_publishes_exclusion_without_any_generation(self):
        from test_tfl_pricing import general_fixture, document
        from types import SimpleNamespace
        for index, script in enumerate(TFL):
            module = load_script(script)
            output = self.base / ('tfl-output-'+str(index))
            payload = {'data':[{'reasoning_capabilities': {'supported_efforts': ['medium']}, 'id':'qwen3.8-flash','context_length':1_000_000},
                               {'reasoning_capabilities': {'supported_efforts': ['medium']}, 'id':'mimo-v2.5','context_length':1_000_000}]}
            router = {'data':[{'reasoning_capabilities': {'supported_efforts': ['medium']}, 'id':'xiaomi/mimo-v2.5','context_length':1_000_000,
                               'pricing':{'prompt':'0','completion':'0'}},
                              {'id':'~xiaomi/MIMO-V2.5:free'},
                              {'id':'~meta/muse-spark-1.2-contributor'},
                              {'reasoning_capabilities': {'supported_efforts': ['medium']}, 'id':'~unbiased/pareto-latest','context_length':1_000_000,
                               'pricing':{'prompt':'0.0000001','completion':'0.0000001'}}]}
            general, metadata, pricing = general_fixture(module)
            general['data'].append({'reasoning_capabilities': {'supported_efforts': ['medium']}, 'id':'mimo-v2.5-free','context_length':1_000_000})
            with ExitStack() as stack:
                for name, value in {
                    'parse_args':SimpleNamespace(policy_option=None,policy='auto',timeout=1,output_dir=output),
                    'select_secret':('mode1','offline'), 'fetch_models':payload,
                    'fetch_go_metadata':{},
                    'fetch_go_pricing':{'source':module.SOURCE_URL,'retrieved_at':'fixture','models':module.parse_go_pricing(document([('Qwen3.8 Flash','$0.1','$0.2','-','-')]))},
                    'fetch_opencode_models':general, 'fetch_opencode_metadata':metadata,
                    'fetch_opencode_pricing':pricing, 'fetch_openrouter_models':router,
                }.items():
                    stack.enter_context(patch.object(module,name,return_value=value))
                stack.enter_context(patch.object(module,'urlopen',side_effect=AssertionError('Réseau interdit')))
                generation = stack.enter_context(patch.object(module,'evaluate_free',side_effect=AssertionError('Génération interdite')))
                stack.enter_context(patch('sys.stdout',new_callable=io.StringIO))
                self.assertEqual(module.main(),0)
                generation.assert_not_called()
            data=json.loads((output/'tfl.json').read_text())
            for section in ('opencode_go','openrouter'):
                self.assertEqual(len(data[section]['models']),1)
                self.assertTrue(any('LM' in item['reason'] for item in data[section]['excluded_models']))
            self.assertEqual(data['free_performance_results'],[])
            self.assertEqual(data['lm_blacklist']['model_ids'],['mimo-v2.5', 'muse-spark-1.2-contributor'])
            self.assertNotIn('blacklists', data)
            self.assertNotIn('blacklist', data['openrouter'])
            self.assertNotIn('permanent_model_ids', data['lm_blacklist'])
            self.assertEqual(data['openrouter']['models'][0]['id'], '~unbiased/pareto-latest')
            self.assertEqual({item['id'] for item in data['openrouter']['excluded_models']},
                             {'xiaomi/mimo-v2.5', '~xiaomi/MIMO-V2.5:free',
                              '~meta/muse-spark-1.2-contributor'})
            self.assertNotIn('mimo-v2.5',(output/'tfl.md').read_text())

    def test_invalid_lm_stops_tfl_and_pllm_before_any_provider(self):
        self.write('{')
        for script in (*TFL, *PLLM):
            module = load_script(script)
            with ExitStack() as stack:
                lookup = stack.enter_context(patch.object(module.subprocess, 'run'))
                network = stack.enter_context(patch.object(module, 'urlopen' if script in TFL else 'get'))
                if script in TFL:
                    stack.enter_context(patch.object(module, 'parse_args', return_value=type('Args', (), {'policy_option':None,'policy':'auto'})()))
                    stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 1)
                else:
                    with self.assertRaises(RuntimeError):
                        module.main()
                lookup.assert_not_called()
                network.assert_not_called()
        self.assertEqual(self.path.read_text(), '{')

    def test_pllm_old_catalog_is_filtered_in_all_catalog_modes(self):
        path = self.catalog()
        for script in PLLM:
            module = load_script(script)
            for priority in range(1, 7):
                model = module.initial_model(priority, module.POLICY_PROVIDERS[priority-1])
                model['candidate_exclusions'] = []
                category = 'free' if priority in (3, 4, 6) else 'paid'
                with patch.object(module.performance, 'fetch_eur_rates', return_value=FX):
                    if priority == 5:
                        with patch.object(module, 'get', return_value=self.openrouter_live(json.loads(path.read_text())['openrouter']['models'])):
                            candidates = module.candidates_for(model, category, path, key='offline')
                    else:
                        candidates = module.candidates_for(model, category, path)
                self.assertTrue(candidates)
                self.assertTrue(all(not self.m.is_blocked(item['model_id']) for item in candidates))
                self.assertTrue(model['candidate_exclusions'])

    def test_pllm_forced_ranks_reject_without_substitution(self):
        path = self.catalog()
        for script in PLLM:
            module = load_script(script)
            for priority in range(1, 7):
                model = module.initial_model(priority, module.POLICY_PROVIDERS[priority-1])
                model['candidate_exclusions'] = []
                category = 'free' if priority in (3, 4, 6) else 'paid'
                with patch.object(module.performance, 'fetch_eur_rates', return_value=FX):
                    if priority == 5:
                        with patch.object(module, 'get', return_value=self.openrouter_live(json.loads(path.read_text())['openrouter']['models'])):
                            with self.assertRaises(RuntimeError):
                                module.candidates_for(model, category, path, forced={'mode':model['mode'],'rank':1}, key='offline')
                    elif priority != 6:
                        with self.assertRaises(RuntimeError):
                            module.candidates_for(model, category, path, forced={'mode':model['mode'],'rank':1})
            self.assertEqual(module.tfl_opencode_model_at(2,path)[0]['id'], 'allowed')
            with self.assertRaises(RuntimeError):
                module.tfl_opencode_model_at(1,path)
            self.assertEqual(module.next_tfl_opencode_model('allowed',path)['id'], 'allowed-free')

    def test_mode7_and_generation_guards_cannot_use_blacklisted_memory(self):
        self.m.update_models('ADD', 'deepseek-v4-flash')
        for script in PLLM:
            module = load_script(script)
            model = module.initial_model(7,'deepseek')
            with self.assertRaises(RuntimeError):
                module.candidates_for(model,'paid',None)
            model.update(model_id='mimo-v2.5')
            with patch.object(module,'benchmark') as benchmark, patch.object(module,'quota') as quota:
                with self.assertRaises(RuntimeError):
                    module.evaluate_candidate(model,'offline','paid',{'policies':{'mode7':{'last_successful_max_tokens':8192}}},None)
            benchmark.assert_not_called()
            quota.assert_not_called()
            with patch.object(module.performance,'run_benchmark') as raw:
                with self.assertRaises(RuntimeError):
                    module.benchmark(model,'offline',8192,{})
            raw.assert_not_called()

    def test_pllm_marked_catalog_and_generation_guards_keep_lm_exclusions(self):
        self.m.update_models('ADD', 'custom')
        path = self.catalog()
        content = json.loads(path.read_text())
        blocked = ('~xiaomi/MIMO-V2.5:free', '~meta/muse-spark-1.2-contributor',
                   '~vendor/custom-free')
        content['openrouter']['models'] = [row(identifier, 'openrouter') for identifier in
                                           (*blocked, '~unbiased/pareto-latest')]
        path.write_text(json.dumps(content))
        for script in PLLM:
            module = load_script(script)
            model = module.initial_model(5, 'openrouter')
            model['candidate_exclusions'] = []
            with patch.object(module.performance, 'fetch_eur_rates', return_value=FX), \
                    patch.object(module, 'get', return_value=self.openrouter_live(content['openrouter']['models'])):
                candidates = module.candidates_for(model, 'paid', path, key='offline')
            self.assertEqual([item['model_id'] for item in candidates], ['~unbiased/pareto-latest'])
            self.assertEqual(len(model['candidate_exclusions']), 3)
            for identifier in blocked:
                model.update(model_id=identifier)
                with patch.object(module, 'benchmark') as benchmark, patch.object(module, 'quota') as quota:
                    with self.assertRaises(RuntimeError):
                        module.evaluate_candidate(model, 'offline', 'paid', {}, None)
                benchmark.assert_not_called()
                quota.assert_not_called()
                with patch.object(module.performance, 'run_benchmark') as raw:
                    with self.assertRaises(RuntimeError):
                        module.benchmark(model, 'offline', 8192, {})
                raw.assert_not_called()

    def test_unvisited_historical_winner_and_candidates_are_invalidated(self):
        for script in PLLM:
            module = load_script(script)
            state = module.load_current()
            model = state['models'][4]
            model.update(model_id='xiaomi/mimo-v2.5', model='MiMo', state='Valide', selected=True,
                         candidate_results=[{'model_id':'mimo-v2.5'}, {'model_id':'allowed'}],
                         ttft_seconds=1, tokens_per_second=999, evaluated_this_run=False)
            module.sanitize_blacklisted_history(state, self.m.load_models())
            self.assertEqual(model['state'],'Invalide')
            self.assertFalse(model['selected'])
            self.assertIsNone(model['ttft_seconds'])
            self.assertEqual(model['model_id'],'Non évalué')
            self.assertEqual([item['model_id'] for item in model['candidate_results']], ['allowed'])
            self.assertTrue(model['candidate_exclusions'])

    def test_actual_pllm_dispatch_never_benchmarks_old_catalog_exclusion(self):
        fixture = qualification.ExtensionQualificationTests()
        self.addCleanup(fixture.doCleanups)
        for script in PLLM:
            module, path = fixture.workspace(script)
            content = json.loads(path.read_text())
            content['opencode_go']['models'].insert(0, row('mimo-v2.5'))
            path.write_text(json.dumps(content))
            result, calls = fixture.run_evaluation(module, path, active=True)
            self.assertEqual(result['selected_mode'],'mode1')
            self.assertEqual(result['models'][0]['model_id'],'first')
            self.assertFalse(any(call[:2]==('benchmark','mimo-v2.5') for call in calls))

    def test_distribution_parity_versions_and_cm_entry(self):
        self.assertEqual(len({path.read_bytes() for path in HELPERS}),1)
        self.assertEqual((ROOT/'.agents/skills/lm').resolve(), ROOT/'skills/lm')
        for filename in ('SKILL.md','agents/openai.yaml','scripts/lm.py','scripts/model_blacklist.py'):
            self.assertEqual((ROOT/'skills/lm'/filename).read_bytes(),(ROOT/'plugins/lm/skills/lm'/filename).read_bytes())
        cm = (ROOT/'skills/cm/SKILL.md').read_bytes()
        self.assertEqual(cm,(ROOT/'plugins/cm/skills/cm/SKILL.md').read_bytes())
        self.assertIn(b'| LM |',cm)
        self.assertIn(b'/LM',cm)
        plugins = json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())['plugins']
        self.assertEqual(len(plugins),6)
        self.assertIn('lm',{item['name'] for item in plugins})
        for item in plugins:
            manifest = json.loads((ROOT/item['source']['path']/'.codex-plugin/plugin.json').read_text())
            self.assertEqual(manifest['version'],'0.7.25')


if __name__ == '__main__':
    unittest.main()
