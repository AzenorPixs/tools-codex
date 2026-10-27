"""Qualification tarifaire TFL déterministe, sans réseau ni trousseau."""

from eur_fixtures import FX

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.error import URLError


ROOT = Path(__file__).resolve().parents[1]
OPENROUTER_FIXTURE_IDS = ('fixture/first', 'fixture/second', 'fixture/third')
SCRIPTS = (ROOT / 'skills/tfl/scripts/test_fournisseur_llm.py',
           ROOT / 'plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py')


def load_script(path):
    spec = importlib.util.spec_from_file_location('tfl_pricing', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def table(rows, headers=('Model', 'Input', 'Output', 'Cached Read', 'Cached Write')):
    return ('<table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers)
            + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
                      for row in rows) + '</tbody></table>')


def document(rows):
    return '<p>Token prices are per 1M tokens.</p>' + table(rows)


def general_fixture(module):
    return (
        {'retrieved_at': '2026-10-25T01:00:00+02:00',
         'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'general-model', 'context_length': 1_000_000}]},
        {'source': module.CONTEXT_METADATA_URL, 'provider_id': 'opencode',
         'models_api': module.OPENCODE_API_URL, 'retrieved_at': '2026-10-25T01:00:00+02:00',
         'provider': {'api': 'https://opencode.ai/general-fixture/v1', 'npm': '@ai-sdk/openai-compatible'},
         'models': {'general-model': {'modalities': {'input': ['text'], 'output': ['text']}}}},
        {'source': module.OPENCODE_SOURCE_URL, 'retrieved_at': '2026-10-25T01:00:00+02:00',
         'models': module.parse_go_pricing(document([('General Model', '$0.1', '$0.2', '-', '-')]))},
    )


def mock_general_collection(module, stack):
    stack.enter_context(patch.object(module.performance, "fetch_eur_rates", return_value=FX))
    payload, metadata, pricing = general_fixture(module)
    stack.enter_context(patch.object(module, 'fetch_opencode_models', return_value=payload))
    stack.enter_context(patch.object(module, 'fetch_opencode_metadata', return_value=metadata))
    stack.enter_context(patch.object(module, 'fetch_opencode_pricing', return_value=pricing))


class PricingTests(unittest.TestCase):
    def modules(self):
        return [(path, load_script(path)) for path in SCRIPTS]

    def pricing(self, module, rows=None):
        rows = rows or [('MiniMax M3.1 Flash', '$0.15', '$0.60', '$0.015', '-')]
        return {'source': 'https://opencode.ai/docs/go/',
                'retrieved_at': '2026-10-25T01:00:00+02:00',
                'models': module.parse_go_pricing(document(rows))}

    def payload(self, model_id='minimax-m3.1-flash'):
        return {'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': model_id, 'context_length': 1_000_000}]}

    def openrouter(self, module):
        return {'pricing_source': module.OPENROUTER_API_URL,
                'pricing_retrieved_at': '2026-10-25T01:00:01+02:00',
                'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': model_id, 'context_length': 1_000_000,
                          'architecture': {'output_modalities': ['text']},
                          'pricing': {'prompt': '0.00000003', 'completion': '0.00000013',
                                      'input_cache_read': '0.000000006'}}
                         for model_id in OPENROUTER_FIXTURE_IDS]}

    def setup_main(self, module, output, stack):
        mock_general_collection(module, stack)
        stack.enter_context(patch.dict(module.os.environ, {'CODEX_HOME': str(output / 'codex-profile')}, clear=True))
        stack.enter_context(patch.object(module, 'urlopen', side_effect=AssertionError('réseau interdit')))
        stack.enter_context(patch.object(module, 'parse_args', return_value=SimpleNamespace(
            policy_option=None, policy='auto', timeout=1, output_dir=output)))
        stack.enter_context(patch.object(module, 'select_secret', return_value=('mode1', 'offline-fixture')))
        stack.enter_context(patch.object(module, 'fetch_models', return_value=self.payload()))
        stack.enter_context(patch.object(module, 'fetch_go_metadata', return_value={}))
        stack.enter_context(patch.object(module, 'fetch_openrouter_models', return_value=self.openrouter(module)))

    def test_new_model_is_ranked_without_static_reference(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                rows, excluded = module.build_rows(self.payload(), {}, self.pricing(module))
                self.assertEqual(excluded, [])
                self.assertEqual(rows[0]['id'], 'minimax-m3.1-flash')
                self.assertEqual(rows[0]['reference_average_usd_per_million_tokens'], 0.375)
                self.assertEqual(rows[0]['reference_pricing_usd_per_million_tokens']['cache_read_off_peak'], 0.015)
                self.assertIsNone(rows[0]['quota_estimates_requests']['monthly'])
                self.assertIsNone(rows[0]['api_endpoint'])
                self.assertEqual(rows[0]['routing_status'], 'not_verified')
                self.assertTrue(rows[0]['routing_warning'])
                self.assertIn('minimax-m3.1-flash', module.format_opencode_table(rows, 'mode1', 'fixture'))

    def test_changed_go_prices_are_used_on_next_collection(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                low = self.pricing(module)
                high = self.pricing(module, [('MiniMax M3.1 Flash', '$0.30', '$1.20', '-', '-')])
                self.assertEqual(len(module.build_rows(self.payload(), {}, low)[0]), 1)
                rows, excluded = module.build_rows(self.payload(), {}, high)
                self.assertEqual(rows, [])
                self.assertEqual(excluded[0]['reference_average_usd_per_million_tokens'], 0.75)

    def test_unknown_price_and_context_are_excluded(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                rows, excluded = module.build_rows(self.payload('absent-model'), {}, self.pricing(module))
                self.assertEqual(rows, [])
                self.assertIn('aucun tarif correspondant', excluded[0]['reason'])
                payload = self.payload()
                payload['data'][0]['context_length'] = 200_000
                self.assertIn('inférieur', module.build_rows(payload, {}, self.pricing(module))[1][0]['reason'])

    def test_price_variants_and_context_tiers_are_separate(self):
        rows = [('Model X (≤ 256K tokens)', '$0.1', '$0.2', '$0.01', '$0.02'),
                ('Model X (> 256K tokens)', '$0.3', '$0.6', '$0.03', '$0.06'),
                ('Model Y (Off-Peak)', '$0.1', '$0.2', '-', '-'),
                ('Model Y (Peak)', '$0.5', '$1.0', '$0.05', '-'),
                ('Model Y', '$0.9', '$1.2', '-', '-')]
        for path, module in self.modules():
            with self.subTest(path=path):
                pricing = self.pricing(module, rows)
                x = module.go_reference_prices(pricing['models']['modelx'])
                self.assertAlmostEqual(x['average_off_peak'], 0.45)
                self.assertEqual(x['cache_write_off_peak'], 0.06)
                y = module.go_reference_prices(pricing['models']['modely'])
                self.assertAlmostEqual(y['average_off_peak'], 0.15)
                self.assertEqual(y['average_peak'], 0.75)
                self.assertEqual(y['cache_read_peak'], 0.05)

    def test_duplicate_plans_agree_and_conflicts_fail(self):
        row = [('MiniMax M3.1 Flash', '$0.15', '$0.60', '$0.015', '-')]
        for path, module in self.modules():
            with self.subTest(path=path):
                refs = module.parse_go_pricing(document(row) + table(row))
                self.assertEqual(len(refs['minimaxm31flash']['variants']), 1)
                conflict = [('MiniMax M3.1 Flash', '$0.16', '$0.60', '$0.015', '-')]
                with self.assertRaisesRegex(RuntimeError, 'contradictoires'):
                    module.parse_go_pricing(document(row) + table(conflict))

    def test_struck_prices_are_ignored_and_free_is_explicit(self):
        rows = [('Model X (50% off)', '<del>$4.00</del> $2.00', '<s>$20.00</s>$10.00', '-', '-'),
                ('Model Free', 'Free', 'Free', 'Free', '-')]
        for path, module in self.modules():
            with self.subTest(path=path):
                refs = self.pricing(module, rows)['models']
                self.assertEqual(module.go_reference_prices(refs['modelx'])['input_off_peak'], 2)
                self.assertEqual(module.go_reference_prices(refs['modelfree'])['average_off_peak'], 0)

    def test_nonrecognized_format_unit_and_missing_columns_fail(self):
        invalid = ['<h1>Maintenance</h1>',
                   document([('Model X', '$0.1', '$0.2', '-', '-')]).replace('1M', '1K'),
                   document([('Model X', '$0.1', '$0.2', '-', '-')]).replace('<th>Output</th>', '<th>Unknown</th>'),
                   document([('Model X', '$0.1')]),
                   document([('Model X', '$0.1', '$0.2', '-', '-')])[:-8],
                   document([('Model X', '$0.1', '$0.2', '-', '-')]).replace('</tr>', ''),
                   document([('Model X', '$0.1', '$0.2', '-', '-')]).replace('</td>', ''),
                   document([('Model X (unknown tier)', '$0.1', '$0.2', '-', '-')])]
        for path, module in self.modules():
            for html in invalid:
                with self.subTest(path=path, html=html[:60]):
                    with self.assertRaises(RuntimeError):
                        module.parse_go_pricing(html)

    def test_invalid_go_amounts_fail(self):
        for path, module in self.modules():
            for amount in ('NaN', '$Infinity', '$-0.1', '-', '$0.1 $0.2', '€0.15', '$' + '9' * 400):
                with self.subTest(path=path, amount=amount[:30]):
                    with self.assertRaises(RuntimeError):
                        self.pricing(module, [('Model X', amount, '$0.1', '-', '-')])

    def test_ambiguous_names_and_api_ids_fail(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                with self.assertRaisesRegex(RuntimeError, 'ambiguë'):
                    self.pricing(module, [('Model X', '$0.1', '$0.2', '-', '-'),
                                          ('Model-X', '$0.1', '$0.2', '-', '-')])
                payload = self.payload()
                payload['data'].append({'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'minimax_m3.1_flash', 'context_length': 1_000_000})
                with self.assertRaisesRegex(RuntimeError, 'plusieurs identifiants'):
                    module.build_rows(payload, {}, self.pricing(module))

    def test_pricing_fetch_records_source_time_digest_and_size_limit(self):
        class Response(io.BytesIO):
            def geturl(self):
                return 'https://opencode.ai/v2/docs/console/go/'
        html = document([('MiniMax M3.1 Flash', '$0.15', '$0.60', '-', '-')]).encode()
        for path, module in self.modules():
            with self.subTest(path=path):
                with patch.object(module, 'urlopen', return_value=Response(html)) as fetch:
                    pricing = module.fetch_go_pricing(3)
                self.assertEqual(pricing['source'], 'https://opencode.ai/v2/docs/console/go/')
                self.assertTrue(pricing['retrieved_at'])
                self.assertEqual(len(pricing['sha256']), 64)
                self.assertEqual(fetch.call_args.kwargs['timeout'], 3)
                for raw, message in ((b'x' * (2 * 1024 * 1024 + 1), 'volumineuse'), (b'\xff', 'UTF-8')):
                    with patch.object(module, 'urlopen', return_value=Response(raw)):
                        with self.assertRaisesRegex(RuntimeError, message):
                            module.fetch_go_pricing(3)

    def test_openrouter_refresh_provenance_cache_and_context_overrides(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload = self.openrouter(module)
                payload['data'][0]['pricing']['overrides'] = [{
                    'min_prompt_tokens': 32_000, 'prompt': '0.0000001',
                    'completion': '0.0000004', 'input_cache_write': '0.000000125'}]
                rows, _ = module.build_openrouter_rows(payload, exchange_rates=FX)
                first = next(r for r in rows if r['id'] == OPENROUTER_FIXTURE_IDS[0])
                self.assertAlmostEqual(first['average'], 0.08)
                self.assertEqual(first['pricing_retrieved_at'], payload['pricing_retrieved_at'])
                self.assertAlmostEqual(first['pricing_details']['base']['input_cache_read'], 0.006)
                self.assertAlmostEqual(first['pricing_details']['overrides'][0]['completion'], 0.4)
                payload['data'][0]['pricing']['completion'] = '0.00000023'
                rows, _ = module.build_openrouter_rows(payload, exchange_rates=FX)
                first = next(r for r in rows if r['id'] == OPENROUTER_FIXTURE_IDS[0])
                self.assertAlmostEqual(first['average'], 0.13)

    def test_invalid_openrouter_prices_and_optional_cache_are_marked(self):
        for path, module in self.modules():
            for value in ('-0.1', True, 'NaN', '1e999'):
                with self.subTest(path=path, value=value):
                    payload = self.openrouter(module)
                    payload['data'][0]['pricing']['prompt'] = value
                    rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                    self.assertEqual(len(rows), 2)
                    self.assertIn('non vérifiable', excluded[0]['reason'])
            payload = self.openrouter(module)
            payload['data'][0]['pricing']['input_cache_read'] = 'NaN'
            rows, _ = module.build_openrouter_rows(payload, exchange_rates=FX)
            row = next(r for r in rows if r['id'] == OPENROUTER_FIXTURE_IDS[0])
            self.assertIsNone(row['pricing_details']['base']['input_cache_read'])
            self.assertIn('input_cache_read', row['pricing_details']['unverified_fields'])

    def test_openrouter_fetch_records_actual_source_and_time(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                raw = json.dumps(self.openrouter(module)).encode()
                with patch.object(module, 'urlopen', return_value=io.BytesIO(raw)) as fetch:
                    payload = module.fetch_openrouter_models(None, 1)
                self.assertEqual(payload['pricing_source'], module.OPENROUTER_API_URL)
                self.assertEqual(fetch.call_args.args[0].full_url, module.OPENROUTER_API_URL)
                self.assertNotEqual(payload['pricing_retrieved_at'], '2026-10-25T01:00:01+02:00')

    def test_invalid_openrouter_overrides_fail_and_disappearance_is_allowed(self):
        for path, module in self.modules():
            for override in ('invalid', [None], [{}], [{'min_prompt_tokens': -1}],
                             [{'min_prompt_tokens': True}], [{'utc_days': ['invalid']}],
                             [{'utc_start': 100}], [{'utc_start': 2460, 'utc_end': 0}],
                             [{'utc_start': False, 'utc_end': 0}]):
                with self.subTest(path=path, override=override):
                    payload = self.openrouter(module)
                    payload['data'][0]['pricing']['overrides'] = override
                    with self.assertRaisesRegex(RuntimeError, 'tarifaire'):
                        module.build_openrouter_rows(payload, exchange_rates=FX)
            payload = self.openrouter(module)
            payload['data'].pop()
            rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
            self.assertEqual(len(rows), 2)
            self.assertEqual(excluded, [])

    def test_temporal_openrouter_overrides_preserve_utc_conditions_and_base_ranking(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload = self.openrouter(module)
                payload['data'][0]['pricing'] = {
                    'prompt': '0.00000015', 'completion': '0.0000006',
                    'overrides': [
                        {'utc_days': ['saturday', 'sunday'], 'prompt': '0.00000015',
                         'completion': '0.0000006', 'input_cache_read': '0.000000003'},
                        {'utc_days': ['monday'], 'utc_start': 100, 'utc_end': 400,
                         'prompt': '0.0000003', 'completion': '0.0000012'},
                    ]}
                rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                selected = next(r for r in rows if r['id'] == OPENROUTER_FIXTURE_IDS[0])
                self.assertEqual(excluded, [])
                self.assertEqual(selected['average'], 0.375)
                variants = selected['pricing_details']['overrides']
                self.assertEqual(variants[0]['utc_days'], ['saturday', 'sunday'])
                self.assertAlmostEqual(variants[0]['input_cache_read'], 0.003)
                self.assertNotIn('min_prompt_tokens', variants[0])
                self.assertEqual(variants[1]['utc_start'], 100)
                self.assertEqual(variants[1]['utc_end'], 400)
                self.assertAlmostEqual(variants[1]['completion'], 1.2)

    def test_dynamic_catalog_keeps_new_free_and_boundary_models_with_audited_exclusions(self):
        def model(model_id, **changes):
            value = {'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': model_id, 'context_length': 1_000_000,
                     'pricing': {'prompt': '0.0000001', 'completion': '0.0000002'},
                     'architecture': {'input_modalities': ['text'], 'output_modalities': ['text']}}
            value.update(changes)
            return value

        for path, module in self.modules():
            with self.subTest(path=path):
                payload = {'data': [
                    model('new/free', pricing={'prompt': '0', 'completion': '0'}),
                    model('new/boundary', pricing={'prompt': '0.0000005', 'completion': '0.0000005'}),
                    model('new/multimodal', architecture={'input_modalities': ['text', 'image', 'audio'],
                                                        'output_modalities': ['text']}),
                    model('new/unknown-output', architecture={}),
                    model('new/expensive', pricing={'prompt': '0.0000005', 'completion': '0.0000006'}),
                    model('new/short-context', context_length=999_999),
                    model('new/unknown-context', context_length=None),
                    model('new/unknown-price', pricing={}),
                    model('meta/muse-spark-1.2-contributor'),
                    *[model('new/' + modality, architecture={'output_modalities': [modality]})
                      for modality in ('audio', 'video', 'speech', 'sound')],
                ]}
                rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                self.assertEqual([r['id'] for r in rows],
                                 ['new/free', 'new/multimodal', 'new/unknown-output', 'new/boundary'])
                self.assertEqual([r['rank'] for r in rows], [1, 2, 3, 4])
                self.assertEqual(rows[-1]['average'], 0.5)
                self.assertEqual(rows[2]['output_label'], 'Non vérifié')
                self.assertEqual(len(rows) + len(excluded), len(payload['data']))
                reasons = {m['id']: m['reason'] for m in excluded}
                self.assertIn('seuil maximal', reasons['new/expensive'])
                self.assertIn('contexte', reasons['new/short-context'])
                self.assertIn('contexte', reasons['new/unknown-context'])
                self.assertIn('non vérifiable', reasons['new/unknown-price'])
                self.assertEqual(reasons['meta/muse-spark-1.2-contributor'], 'liste noire LM')
                for modality in ('audio', 'video', 'speech', 'sound'):
                    self.assertIn('sortie', reasons['new/' + modality])
                reversed_rows, _ = module.build_openrouter_rows({'data': list(reversed(payload['data']))}, exchange_rates=FX)
                self.assertEqual([r['id'] for r in reversed_rows], [r['id'] for r in rows])

    def test_entire_catalog_is_examined_beyond_one_thousand_models(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                prototype = self.openrouter(module)['data'][0]
                payload = {'data': [{**prototype, 'id': f'new/model-{index:04}'} for index in range(1005)]}
                rows, excluded = module.build_openrouter_rows(payload, exchange_rates=FX)
                self.assertEqual(len(rows), 1005)
                self.assertEqual(rows[-1]['id'], 'new/model-1004')
                self.assertEqual(rows[-1]['rank'], 1005)
                self.assertEqual(excluded, [])

    def test_arrival_and_disappearance_recompute_selection_without_old_ids(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload = self.openrouter(module)
                before, _ = module.build_openrouter_rows(payload, exchange_rates=FX)
                old_id = before[0]['id']
                payload['data'] = [m for m in payload['data'] if m['id'] != old_id]
                payload['data'].append({**payload['data'][0], 'id': 'new/cheaper',
                                        'pricing': {'prompt': '0', 'completion': '0'}})
                after, _ = module.build_openrouter_rows(payload, exchange_rates=FX)
                self.assertEqual(after[0]['id'], 'new/cheaper')
                self.assertNotIn(old_id, [r['id'] for r in after])

    def test_main_failure_preserves_previous_reports_without_static_fallback(self):
        for path, module in self.modules():
            for failure in (URLError('fixture'), RuntimeError('format tarifaire inconnu')):
                with self.subTest(path=path, failure=type(failure).__name__):
                    with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                        output = Path(tmp)
                        for name in ('tfl.json', 'tfl.md'):
                            (output / name).write_text('previous-report', encoding='utf-8')
                        self.setup_main(module, output, stack)
                        stack.enter_context(patch.object(module, 'fetch_go_pricing', side_effect=failure))
                        error = stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                        with patch.object(module, 'atomic_write') as write:
                            self.assertEqual(module.main(), 1)
                            write.assert_not_called()
                        self.assertIn('Erreur TFL', error.getvalue())
                        for name in ('tfl.json', 'tfl.md'):
                            self.assertEqual((output / name).read_text(), 'previous-report')

    def test_openrouter_collection_failure_preserves_both_reports(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                    output = Path(tmp)
                    for name in ('tfl.json', 'tfl.md'):
                        (output / name).write_text('previous-report', encoding='utf-8')
                    self.setup_main(module, output, stack)
                    stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=self.pricing(module)))
                    stack.enter_context(patch.object(module, 'fetch_openrouter_models', side_effect=URLError('fixture')))
                    stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 1)
                    for name in ('tfl.json', 'tfl.md'):
                        self.assertEqual((output / name).read_text(), 'previous-report')

    def test_main_success_publishes_both_provenances_without_secrets(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                    output = Path(tmp)
                    self.setup_main(module, output, stack)
                    stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=self.pricing(module)))
                    stdout = stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 0)
                    raw = (output / 'tfl.json').read_text()
                    data = json.loads(raw)
                    self.assertEqual(data['opencode_go']['pricing_reference']['retrieved_at'],
                                     '2026-10-25T01:00:00+02:00')
                    self.assertEqual(data['openrouter']['pricing_retrieved_at'],
                                     '2026-10-25T01:00:01+02:00')
                    self.assertEqual(data['openrouter']['selection'], 'live-api-context-cost-modalities')
                    self.assertEqual(data['openrouter']['source_model_count'], 3)
                    self.assertNotIn('offline-fixture', raw + stdout.getvalue())
                    markdown = (output / 'tfl.md').read_text()
                    self.assertLess(markdown.index('OpenCode Go'), markdown.index('OpenRouter'))
                    self.assertIn('0.375', markdown)

    def test_no_dynamic_result_publishes_empty_router_and_keeps_other_results(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload = self.openrouter(module)
                for model in payload['data']:
                    model['pricing'] = {'prompt': '1', 'completion': '1'}
                with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                    output = Path(tmp)
                    for name in ('tfl.json', 'tfl.md'):
                        (output / name).write_text('previous-report', encoding='utf-8')
                    self.setup_main(module, output, stack)
                    stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=self.pricing(module)))
                    stack.enter_context(patch.object(module, 'fetch_openrouter_models', return_value=payload))
                    stdout = stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 0)
                    catalog = json.loads((output / 'tfl.json').read_text())
                    self.assertEqual(catalog['openrouter']['models'], [])
                    self.assertEqual(catalog['openrouter']['selection_status'], 'empty')
                    self.assertEqual(catalog['openrouter']['excluded_model_count'], 3)
                    self.assertEqual(sum(catalog['openrouter']['exclusion_summary'].values()), 3)
                    self.assertTrue(catalog['opencode_go']['models'])
                    self.assertNotIn('opencode', catalog)
                    self.assertIn('Aucun modèle admissible.', stdout.getvalue())
                    self.assertIn('Exclusions :', stdout.getvalue())
                    self.assertNotIn('previous-report', (output / 'tfl.md').read_text())


if __name__ == '__main__':
    unittest.main()
