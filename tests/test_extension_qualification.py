"""Qualification hors ligne des correctifs CGP dans les deux distributions."""

from eur_fixtures import FX

from contextlib import ExitStack
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from test_tfl_pricing import mock_general_collection
from unittest.mock import patch
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
OPENROUTER_FIXTURE_IDS = ('fixture/first', 'fixture/second', 'fixture/third')
PLLM = (ROOT / 'skills/pllm/scripts/evaluate.py',
        ROOT / 'plugins/pllm/skills/pllm/scripts/evaluate.py')
TFL = (ROOT / 'skills/tfl/scripts/test_fournisseur_llm.py',
       ROOT / 'plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py')


def load_script(path):
    spec = importlib.util.spec_from_file_location('extension_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate(name):
    return {'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': name, 'available': True, 'api_endpoint': 'https://opencode.ai/zen/go/v1/responses',
            'api_protocol': 'responses', 'context_length': 1_000_000,
            'reference_pricing_usd_per_million_tokens': {'input_off_peak': 0.1, 'output_off_peak': 0.2}}


def rate_limit():
    error = HTTPError('https://example.invalid', 429, 'fixture', {}, io.BytesIO())
    error.close()
    return error


class ExtensionQualificationTests(unittest.TestCase):
    def workspace(self, script):
        temporary = tempfile.TemporaryDirectory(prefix='qualification-', dir=ROOT / 'tests')
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        # Reproduce two plugin installations with separate version directories.
        installed = base / 'pllm' / 'version-a' / 'skills' / 'pllm' / 'scripts' / script.name
        installed.parent.mkdir(parents=True)
        installed.write_bytes(script.read_bytes())
        installed.with_name('performance.py').write_bytes(script.with_name('performance.py').read_bytes())
        installed.with_name('model_blacklist.py').write_bytes(script.with_name('model_blacklist.py').read_bytes())
        installed.with_name('model_evidence.py').write_bytes(script.with_name('model_evidence.py').read_bytes())
        module = load_script(installed)
        module.MEMORY_PATH = module.ROOT / 'data/pllm-performance-memory.json'
        catalog = base / 'tfl' / 'version-b' / 'skills' / 'tfl' / 'data' / 'tfl.json'
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({'generated_at': 'fixture-date',
                                      'opencode_go': {'models': [candidate('first'), candidate('second')]},
                                      'openrouter': {'models': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'router-fixture', 'context_length': 1_000_000,
                                                                 'input_price': 0.1, 'output_price': 0.2}]}}), encoding='utf-8')
        return module, catalog

    def run_evaluation(self, module, catalog, behavior=None, quota_failure=None, **kwargs):
        calls = []

        def quota(model, key):
            calls.append(('quota', model['model_id']))
            if model['model_id'] == quota_failure:
                raise RuntimeError('Quota indisponible')
            model['quotas'] = ({period: {'percent': 10} for period in ('rolling', 'weekly', 'monthly')}
                               if model['provider'] == 'opencodego' else {'balance': 1, 'currency': 'USD'})

        def benchmark(model, key, budget, metadata, session_id=None):
            calls.append(('benchmark', model['model_id'], budget))
            model['performance_test'] = {'status': 'running', 'max_tokens': budget}
            if behavior:
                behavior(model, budget)
            model.update(ttft_seconds=5 if model['mode'] in module.FREE_MODES else 70.4, tokens_per_second=25)
            model['performance_test']['status'] = 'completed'
            return True

        with ExitStack() as stack:
            stack.enter_context(patch.object(module.performance, "fetch_eur_rates", return_value=FX))
            stack.enter_context(patch.object(module.subprocess, 'run', return_value=SimpleNamespace(returncode=0, stdout=b'offline-fixture')))
            stack.enter_context(patch.object(module, 'quota', side_effect=quota))
            stack.enter_context(patch.object(module, 'benchmark', side_effect=benchmark))
            stack.enter_context(patch.object(module, 'get', return_value={'data': [
                {'id': 'router-fixture', 'reasoning': {'supported_efforts': ['high']}}]}))
            stack.enter_context(patch.object(module, 'exchange_rates', return_value={'rates': {'USD': 1}}))
            stack.enter_context(patch.object(module.urllib.request, 'urlopen', side_effect=AssertionError('Réseau interdit pendant le test')))
            stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
            module.main(tfl_catalog=catalog, **kwargs)
        result = json.loads((module.ROOT / 'data/pllm-current.json').read_text(encoding='utf-8'))
        return result, calls

    def test_catalog_option_and_default_for_separate_plugins(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                self.assertEqual(module.tfl_opencode_model_at(1, catalog)[0]['id'], 'first')
                self.assertEqual(module.next_tfl_opencode_model('first', catalog)['id'], 'second')
                default = module.ROOT.parent / 'tfl/data/tfl.json'
                default.parent.mkdir(parents=True)
                default.write_bytes(catalog.read_bytes())
                self.assertEqual(module.tfl_opencode_model_at(1)[0]['id'], 'first')
                help_result = subprocess.run([sys.executable, '-B', str(module.__file__), '--help'], capture_output=True, text=True, check=True)
                self.assertIn('--tfl-catalog', help_result.stdout)

    def test_missing_or_malformed_catalog_is_explicit(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                with self.assertRaisesRegex(RuntimeError, 'Catalogue TFL absent'):
                    module.tfl_opencode_model_at(1, catalog.with_name('absent.json'))
                for content in ('{', '[]', '{"opencode_go": []}', '{"x": NaN}', '{"x": 1e999}'):
                    catalog.write_text(content, encoding='utf-8')
                    with self.assertRaises(RuntimeError):
                        module.tfl_opencode_model_at(1, catalog)

    def test_fresh_start_has_no_invented_results(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                state = module.load_current()
                self.assertEqual([m['mode'] for m in state['models']], [f'mode{i}' for i in range(1, 7)])
                self.assertIsNone(state['selected_mode'])
                self.assertTrue(all(m['state'] == 'Invalide' and m['quotas'] is None and m['ttft_seconds'] is None for m in state['models']))
                self.assertFalse((module.ROOT / 'data').exists())
                result, calls = self.run_evaluation(module, catalog, active=True)
                self.assertEqual(result['selected_mode'], 'mode1')
                self.assertEqual(calls, [('quota', 'Non évalué'), ('quota', 'first'), ('benchmark', 'first', 1024)])
                self.assertTrue(all(not m['evaluated_this_run'] for m in result['models'][1:]))
                self.assertTrue((module.ROOT / 'data/pllm-performance-memory.json').exists())

    def test_existing_state_is_loaded_without_replacement(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, _ = self.workspace(script)
                state = module.load_current()
                state['preserved_marker'] = 'fixture'
                current = module.ROOT / 'data/pllm-current.json'
                current.parent.mkdir()
                content = json.dumps(state).encode()
                current.write_bytes(content)
                self.assertEqual(module.load_current(), state)
                self.assertEqual(current.read_bytes(), content)

    def test_corrupt_state_is_not_published_or_overwritten(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                current = module.ROOT / 'data/pllm-current.json'
                current.parent.mkdir()
                invalid = module.load_current()
                del invalid['models'][0]['state']
                for content in (b'{', b'{}', b'{"models": [1, 2, 3, 4]}', b'{"x": NaN}', b'{"x": 1e999}', json.dumps(invalid).encode()):
                    current.write_bytes(content)
                    with patch.object(module, 'publish') as publish, patch.object(module.subprocess, 'run') as lookup:
                        with self.assertRaisesRegex(RuntimeError, 'Historique PLLM'):
                            module.main(tfl_catalog=catalog)
                        publish.assert_not_called()
                        lookup.assert_not_called()
                    self.assertEqual(current.read_bytes(), content)

    def test_openrouter_uses_explicit_catalog(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                result, calls = self.run_evaluation(module, catalog, forced={'mode': 'mode5'})
                self.assertEqual(result['selected_mode'], 'mode5')
                self.assertEqual(calls, [('quota', 'Non évalué'), ('quota', 'router-fixture'), ('benchmark', 'router-fixture', 1024)])

    def test_all_modes_can_start_without_a_current_file(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                payload = json.loads(catalog.read_text())
                free = candidate('free-fixture')
                free['reference_pricing_usd_per_million_tokens'] = {'input_off_peak': 0, 'output_off_peak': 0}
                payload['opencode_go']['models'].append(free)
                catalog.write_text(json.dumps(payload))
                result, calls = self.run_evaluation(module, catalog)
                self.assertTrue(all(m['evaluated_this_run'] for m in result['models']))
                self.assertTrue(all(m['state'] == 'Valide' for m in result['models'][:5]))
                self.assertEqual(result['models'][5]['state'], 'Invalide')
                self.assertEqual(len(calls), 12)
                self.assertTrue(all(len(m['candidate_results']) == 1 for m in result['models'][:5]))
                self.assertEqual(result['models'][5]['candidate_results'], [])
                self.assertEqual(result['models'][5]['model'], 'Non évalué')
                self.assertIn('HIGH/XHIGH', result['models'][5]['cause'])

    def test_last_tier_fallback_requires_its_own_measurements(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)
                first = module.load_current()['models'][0]
                first.update(model_id='first', api_endpoint='https://opencode.ai/zen/go/v1/responses', api_protocol='responses', throughput_scope='reasoning_and_response')
                memory = {'schema_version': 1, 'policies': {'mode1': {
                    'identity': module.identity(first), 'last_successful_max_tokens': 8192}}}
                module.MEMORY_PATH.parent.mkdir()
                module.MEMORY_PATH.write_text(json.dumps(memory), encoding='utf-8')

                def behavior(model, budget):
                    if model['model_id'] == 'first':
                        raise rate_limit()

                result, calls = self.run_evaluation(module, catalog, behavior, active=True)
                self.assertEqual(calls, [('quota', 'Non évalué'), ('quota', 'first'), ('benchmark', 'first', 8192),
                                         ('quota', 'second'), ('benchmark', 'second', 1024)])
                selected = result['models'][0]
                self.assertEqual((selected['model_id'], selected['state'], selected['last_successful_max_tokens']), ('second', 'Valide', 1024))
                self.assertEqual([a['model_id'] for a in selected['candidate_results']], ['first', 'second'])

    def test_fallback_quota_failure_does_not_benchmark_or_select(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, catalog = self.workspace(script)

                def limited(model, budget):
                    raise rate_limit()

                result, calls = self.run_evaluation(module, catalog, limited, quota_failure='second', active=True)
                self.assertIsNone(result['selected_mode'])
                self.assertFalse(any(c[:2] == ('benchmark', 'second') for c in calls))
                self.assertFalse(module.MEMORY_PATH.exists())

    def test_exhausted_candidates_and_forced_mode_stay_invalid(self):
        for script in PLLM:
            for forced in (None, {'mode': 'mode1'}):
                with self.subTest(script=script, forced=forced):
                    module, catalog = self.workspace(script)

                    def limited(model, budget):
                        raise rate_limit()

                    result, calls = self.run_evaluation(module, catalog, limited, forced=forced, active=True)
                    self.assertIsNone(result['selected_mode'])
                    self.assertFalse(module.MEMORY_PATH.exists())
                    if forced:
                        self.assertEqual(calls[0], ('quota', 'Non évalué'))
                        self.assertTrue(all(c[1] == 'first' for c in calls[1:]))

    def test_active_publication_remains_silent(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, _ = self.workspace(script)
                with patch.object(module, 'exchange_rates', return_value=None), patch('sys.stdout', new_callable=io.StringIO) as output:
                    module.publish(module.load_current(), active=True)
                self.assertEqual(output.getvalue(), '')

    def tfl_payload(self, module):
        return {'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': name, 'context_length': 1_000_000,
                          'pricing': {'prompt': '0.0000001', 'completion': '0.0000002'},
                          'architecture': {'output_modalities': ['text']}}
                         for name in OPENROUTER_FIXTURE_IDS]}

    def tfl_go_pricing(self, module):
        return {'source': module.SOURCE_URL, 'retrieved_at': '2026-10-25T01:00:00+02:00',
                'models': module.parse_go_pricing(
                    '<p>Token prices are per 1M tokens.</p><table><tr><th>Model</th>'
                    '<th>Input</th><th>Output</th></tr><tr><td>Qwen3.8 Flash</td>'
                    '<td>$0.15</td><td>$0.47</td></tr></table>')}

    def test_nonfinite_prices_and_overflows_are_excluded(self):
        for script in TFL:
            module = load_script(script)
            for price in ('NaN', 'Infinity', '-Infinity', '1e999', 10 ** 400, '1e308', '1e302'):
                with self.subTest(script=script, price=str(price)[:20]):
                    payload = self.tfl_payload(module)
                    payload['data'][0]['pricing'] = {'prompt': price, 'completion': price}
                    rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                    self.assertEqual(len(rows), 2)
                    self.assertIn('coût moyen non vérifiable', excluded[0]['reason'])
                    json.dumps({'rows': rows, 'excluded': excluded}, allow_nan=False)

    def test_valid_prices_and_cost_limit_are_preserved(self):
        for script in TFL:
            with self.subTest(script=script):
                module = load_script(script)
                payload = self.tfl_payload(module)
                payload['data'][0]['pricing'] = {'prompt': '0.0000005', 'completion': '0.0000005'}
                rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                self.assertEqual(len(rows), 3)
                self.assertEqual(rows[-1]['average'], 0.5)
                self.assertEqual(excluded, [])
                payload['data'][0]['pricing']['completion'] = '0.0000006'
                rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                self.assertEqual(len(rows), 2)
                self.assertIn('seuil maximal', excluded[0]['reason'])

    def test_non_strict_json_prevents_both_publications(self):
        for script in TFL:
            with self.subTest(script=script):
                module = load_script(script)
                temporary = tempfile.TemporaryDirectory(prefix='tfl-publication-', dir=ROOT / 'tests')
                self.addCleanup(temporary.cleanup)
                output = Path(temporary.name)
                for name in ('tfl.json', 'tfl.md'):
                    (output / name).write_text('preserved-fixture', encoding='utf-8')
                with ExitStack() as stack:
                    stack.enter_context(patch.dict(module.os.environ, {'CODEX_HOME': str(output / 'codex-profile')}, clear=True))
                    stack.enter_context(patch.object(module, 'urlopen', side_effect=AssertionError('Réseau interdit pendant le test')))
                    stack.enter_context(patch.object(module, 'parse_args', return_value=SimpleNamespace(
                        policy_option=None, policy='auto', timeout=1, output_dir=output)))
                    stack.enter_context(patch.object(module, 'select_secret', return_value=('mode1', 'offline-fixture')))
                    stack.enter_context(patch.object(module, 'fetch_models', return_value={'data': []}))
                    stack.enter_context(patch.object(module, 'fetch_go_metadata', return_value={}))
                    stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=self.tfl_go_pricing(module)))
                    mock_general_collection(module, stack)
                    stack.enter_context(patch.object(module, 'build_rows', return_value=([{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'nan-fixture', 'fixture': float('nan')}], [])))
                    stack.enter_context(patch.object(module, 'fetch_openrouter_models', return_value=self.tfl_payload(module)))
                    stack.enter_context(patch.object(module, 'format_opencode_table', return_value='fixture'))
                    write = stack.enter_context(patch.object(module, 'atomic_write'))
                    error = stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 1)
                    write.assert_not_called()
                    self.assertIn('JSON strict', error.getvalue())
                for name in ('tfl.json', 'tfl.md'):
                    self.assertEqual((output / name).read_text(encoding='utf-8'), 'preserved-fixture')

    def test_filtered_catalog_is_published_as_strict_json(self):
        for script in TFL:
            with self.subTest(script=script):
                module = load_script(script)
                temporary = tempfile.TemporaryDirectory(prefix='tfl-filtered-', dir=ROOT / 'tests')
                self.addCleanup(temporary.cleanup)
                output = Path(temporary.name)
                payload = self.tfl_payload(module)
                payload['data'][0]['pricing']['prompt'] = 'NaN'
                with ExitStack() as stack:
                    stack.enter_context(patch.dict(module.os.environ, {'CODEX_HOME': str(output / 'codex-profile')}, clear=True))
                    stack.enter_context(patch.object(module, 'urlopen', side_effect=AssertionError('Réseau interdit pendant le test')))
                    stack.enter_context(patch.object(module, 'parse_args', return_value=SimpleNamespace(
                        policy_option=None, policy='auto', timeout=1, output_dir=output)))
                    stack.enter_context(patch.object(module, 'select_secret', return_value=('mode1', 'offline-fixture')))
                    stack.enter_context(patch.object(module, 'fetch_models', return_value={
                        'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'qwen3.8-flash', 'context_length': 1_000_000}]}))
                    stack.enter_context(patch.object(module, 'fetch_go_metadata', return_value={}))
                    stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=self.tfl_go_pricing(module)))
                    mock_general_collection(module, stack)
                    stack.enter_context(patch.object(module, 'fetch_openrouter_models', return_value=payload))
                    stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 0)

                def reject_constant(value):
                    raise ValueError('Constante JSON non conforme : ' + value)

                result = json.loads((output / 'tfl.json').read_text(encoding='utf-8'), parse_constant=reject_constant)
                self.assertEqual(len(result['openrouter']['models']), 2)
                self.assertIn('coût moyen non vérifiable', result['openrouter']['excluded_models'][0]['reason'])
                self.assertTrue((output / 'tfl.md').exists())


if __name__ == '__main__':
    unittest.main()
