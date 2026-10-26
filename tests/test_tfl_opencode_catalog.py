"""Catalogue général OpenCode : séparation, filtres et publication complète."""

import copy
import io
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.error import URLError

from test_tfl_pricing import SCRIPTS, document, general_fixture, load_script, mock_general_collection


ROOT = Path(__file__).resolve().parents[1]


class GeneralOpenCodeTests(unittest.TestCase):
    def modules(self):
        return [(path, load_script(path)) for path in SCRIPTS]

    def setup_main(self, module, output, stack):
        payload, metadata, pricing = general_fixture(module)
        go_metadata = copy.deepcopy(metadata)
        go_metadata.update(provider_id='opencode-go', models_api=module.API_URL)
        go_metadata['models'] = {'go-only': {'modalities': {'output': ['text']}}}
        go_pricing = {'source': module.SOURCE_URL, 'retrieved_at': metadata['retrieved_at'],
                      'models': module.parse_go_pricing(document([('Go Only', '$0.1', '$0.2', '-', '-')]))}
        stack.enter_context(patch.dict(module.os.environ, {'CODEX_HOME': str(output / 'codex-profile')}, clear=True))
        stack.enter_context(patch.object(module, 'urlopen', side_effect=AssertionError('réseau interdit')))
        stack.enter_context(patch.object(module, 'parse_args', return_value=SimpleNamespace(
            policy_option=None, policy='auto', timeout=1, output_dir=output)))
        stack.enter_context(patch.object(module, 'select_secret', return_value=('mode1', 'offline-fixture')))
        stack.enter_context(patch.object(module, 'fetch_models', return_value={
            'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'go-only', 'context_length': 1_000_000}]}))
        stack.enter_context(patch.object(module, 'fetch_go_metadata', return_value=go_metadata))
        stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=go_pricing))
        mock_general_collection(module, stack)
        stack.enter_context(patch.object(module, 'fetch_openrouter_models', return_value={
            'pricing_source': module.OPENROUTER_API_URL, 'pricing_retrieved_at': metadata['retrieved_at'],
            'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'router-only', 'context_length': 1_000_000,
                      'pricing': {'prompt': '0.0000001', 'completion': '0.0000002'},
                      'architecture': {'output_modalities': ['text']}}]}))

    def test_public_models_request_uses_general_endpoint_without_go_authorization(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, _, _ = general_fixture(module)
                with patch.object(module, 'urlopen', return_value=io.BytesIO(json.dumps(payload).encode())) as fetch:
                    result = module.fetch_opencode_models(2)
                request = fetch.call_args.args[0]
                self.assertEqual(request.full_url, module.OPENCODE_API_URL)
                self.assertIsNone(request.get_header('Authorization'))
                self.assertEqual(result['data'], payload['data'])
                self.assertTrue(result['retrieved_at'])

    def test_invalid_general_api_responses_fail(self):
        for path, module in self.modules():
            for payload in ({}, {'data': {}}, []):
                with self.subTest(path=path, payload=payload):
                    with patch.object(module, 'urlopen', return_value=io.BytesIO(json.dumps(payload).encode())):
                        with self.assertRaisesRegex(RuntimeError, 'catalogue général'):
                            module.fetch_opencode_models(1)
            with patch.object(module, 'urlopen', return_value=io.BytesIO(b'invalid-json')):
                with self.assertRaises(json.JSONDecodeError):
                    module.fetch_opencode_models(1)

    def test_metadata_selects_opencode_provider_instead_of_go(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, _ = general_fixture(module)
                general = {**metadata['provider'], 'models': metadata['models']}
                go = {'npm': '@ai-sdk/anthropic', 'api': 'https://opencode.ai/other-go/v1',
                      'models': {'only-go': {'limit': {'context': 2_000_000}}}}
                raw = json.dumps({'opencode': general, 'opencode-go': go}).encode()
                with patch.object(module, 'urlopen', return_value=io.BytesIO(raw)):
                    collected = module.fetch_opencode_metadata(1)
                self.assertEqual(collected['provider_id'], 'opencode')
                self.assertEqual(collected['models_api'], module.OPENCODE_API_URL)
                self.assertEqual(collected['provider'], metadata['provider'])
                self.assertEqual(collected['models'], metadata['models'])
                self.assertNotIn('only-go', collected['models'])

    def test_general_prices_come_from_general_documentation(self):
        class Response(io.BytesIO):
            def geturl(self):
                return 'https://opencode.ai/v2/docs/console/models/'

        raw = document([('General Model', 'Free', 'Free', 'Free', '-')]).encode()
        for path, module in self.modules():
            with self.subTest(path=path):
                with patch.object(module, 'urlopen', return_value=Response(raw)) as fetch:
                    pricing = module.fetch_opencode_pricing(1)
                self.assertEqual(fetch.call_args.args[0].full_url, module.OPENCODE_SOURCE_URL)
                self.assertEqual(pricing['source'], module.OPENCODE_SOURCE_URL)
                self.assertEqual(pricing['selection_rule'], 'maximum_average_published_context_tier')
                payload, metadata, _ = general_fixture(module)
                row = module.build_rows(payload, metadata, pricing, general_catalog=True)[0][0]
                self.assertEqual(row['reference_average_usd_per_million_tokens'], 0)
                self.assertEqual(row['reference_pricing_usd_per_million_tokens']['input'], 0)

    def test_general_cost_and_context_boundaries(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = general_fixture(module)
                pricing['models'] = module.parse_go_pricing(document([('General Model', '$0.5', '$0.5', '-', '-')]))
                rows, excluded = module.build_rows(payload, metadata, pricing, general_catalog=True)
                self.assertEqual(rows[0]['reference_average_usd_per_million_tokens'], 0.5)
                self.assertEqual(excluded, [])
                payload['data'][0]['context_length'] = 999_999
                rows, excluded = module.build_rows(payload, metadata, pricing, general_catalog=True)
                self.assertEqual(rows, [])
                self.assertIn('contexte', excluded[0]['reason'])
                payload['data'][0]['context_length'] = 1_000_000
                pricing['models'] = module.parse_go_pricing(document([('General Model', '$0.5', '$0.6', '-', '-')]))
                rows, excluded = module.build_rows(payload, metadata, pricing, general_catalog=True)
                self.assertEqual(rows, [])
                self.assertIn('seuil maximal', excluded[0]['reason'])

    def test_free_glm_and_deepseek_200k_are_excluded_without_lowering_context(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = general_fixture(module)
                rows = [('General Model', 'Free', 'Free', '-', '-')]
                for model_id in ('glm-5.3-flash-free', 'deepseek-v4.1-flash-free'):
                    payload['data'].append({'id': model_id})
                    metadata['models'][model_id] = {'limit': {'context': 200_000},
                                                    'modalities': {'output': ['text']}}
                    rows.append((model_id, 'Free', 'Free', '-', '-'))
                pricing['models'] = module.parse_go_pricing(document(rows))
                retained, excluded = module.build_rows(payload, metadata, pricing, general_catalog=True)
                self.assertEqual([m['id'] for m in retained], ['general-model'])
                self.assertEqual(len(excluded), 2)
                self.assertTrue(all(m['context_length'] == 200_000 and 'contexte' in m['reason'] for m in excluded))

    def test_same_id_keeps_independent_prices_routes_and_sources(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, general_metadata, general_pricing = general_fixture(module)
                go_metadata = copy.deepcopy(general_metadata)
                go_metadata.update(provider_id='opencode-go', models_api=module.API_URL)
                go_metadata['provider'] = {'api': 'https://opencode.ai/go-fixture/v1', 'npm': '@ai-sdk/anthropic'}
                go_pricing = copy.deepcopy(general_pricing)
                go_pricing['source'] = module.SOURCE_URL
                general_pricing['models'] = module.parse_go_pricing(document([('General Model', '$0.2', '$0.4', '-', '-')]))
                go_row = module.build_rows(payload, go_metadata, go_pricing)[0][0]
                general_row = module.build_rows(payload, general_metadata, general_pricing, general_catalog=True)[0][0]
                self.assertAlmostEqual(go_row['reference_average_usd_per_million_tokens'], 0.15)
                self.assertAlmostEqual(general_row['reference_average_usd_per_million_tokens'], 0.3)
                self.assertEqual(go_row['api_protocol'], 'messages')
                self.assertEqual(general_row['api_protocol'], 'chat_completions')
                self.assertNotEqual(go_row['api_endpoint'], general_row['api_endpoint'])
                self.assertEqual(go_row['pricing_source'], module.SOURCE_URL)
                self.assertEqual(general_row['pricing_source'], module.OPENCODE_SOURCE_URL)
                with self.assertRaisesRegex(RuntimeError, 'fournisseur incorrect'):
                    module.build_rows(payload, go_metadata, general_pricing, general_catalog=True)

    def test_general_catalog_preserves_blacklist_and_output_filters(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = general_fixture(module)
                payload['data'].extend([{'id': 'muse-spark-1.2-contributor'},
                                        {'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': 'audio-model', 'context_length': 1_000_000}])
                metadata['models']['audio-model'] = {'modalities': {'output': ['text', 'audio']}}
                pricing['models'] = module.parse_go_pricing(document([
                    ('General Model', '$0.1', '$0.2', '-', '-'),
                    ('Audio Model', 'Free', 'Free', '-', '-'),
                ]))
                rows, excluded = module.build_rows(payload, metadata, pricing, general_catalog=True)
                self.assertEqual([m['id'] for m in rows], ['general-model'])
                reasons = {m['id']: m['reason'] for m in excluded}
                self.assertEqual(reasons['muse-spark-1.2-contributor'], 'blacklist permanente')
                self.assertIn('sortie', reasons['audio-model'])

    def test_unknown_general_transport_stays_explicit_without_protocol_guess(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = general_fixture(module)
                metadata['provider']['npm'] = '@unknown/provider'
                row = module.build_rows(payload, metadata, pricing, general_catalog=True)[0][0]
                self.assertIsNone(row['api_endpoint'])
                self.assertIsNone(row['api_protocol'])
                self.assertTrue(row['routing_warning'])
                self.assertEqual(row['output_modalities'], ['text'])

    def test_general_uses_maximum_published_period_while_go_keeps_off_peak(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = general_fixture(module)
                pricing['models'] = module.parse_go_pricing(document([
                    ('General Model (Off-Peak)', '$0.1', '$0.2', '-', '-'),
                    ('General Model (Peak)', '$0.3', '$1.2', '-', '-'),
                ]))
                rows, excluded = module.build_rows(payload, metadata, pricing, general_catalog=True)
                self.assertEqual(rows, [])
                self.assertEqual(excluded[0]['reference_average_usd_per_million_tokens'], 0.75)
                go_metadata = copy.deepcopy(metadata)
                go_metadata['provider_id'] = 'opencode-go'
                go_pricing = copy.deepcopy(pricing)
                go_pricing['source'] = module.SOURCE_URL
                self.assertEqual(len(module.build_rows(payload, go_metadata, go_pricing)[0]), 1)

    def test_general_provenance_uses_general_api_for_explicit_fields(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = general_fixture(module)
                payload['data'][0].update(output_modalities=['text'],
                                          api_endpoint='https://opencode.ai/general-explicit/v1/responses',
                                          api_protocol='responses')
                row = module.build_rows(payload, metadata, pricing, general_catalog=True)[0][0]
                self.assertEqual(row['modalities_metadata']['output']['source'], 'opencode-api')
                self.assertEqual(row['modalities_metadata']['output']['source_api'], module.OPENCODE_API_URL)
                self.assertEqual(row['endpoint_source'], 'opencode-api')
                self.assertEqual(row['routing_metadata']['source_api'], module.OPENCODE_API_URL)

    def test_three_sections_and_tables_preserve_order_columns_and_strict_json(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                    output = Path(tmp)
                    self.setup_main(module, output, stack)
                    stdout = stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 0)
                    raw = (output / 'tfl.json').read_text()
                    catalog = json.loads(raw)
                    self.assertEqual(catalog['order'], ['opencode_go', 'opencode', 'openrouter'])
                    self.assertEqual(catalog['opencode']['models'][0]['id'], 'general-model')
                    self.assertEqual(catalog['opencode']['metadata_provider'], 'opencode')
                    self.assertNotIn('credential_policy', catalog['opencode'])
                    self.assertEqual(catalog['opencode_go']['models'][0]['id'], 'go-only')
                    self.assertEqual(catalog['openrouter']['models'][0]['id'], 'router-only')
                    self.assertNotIn('offline-fixture', raw + stdout.getvalue())
                    markdown = (output / 'tfl.md').read_text()
                    titles = [markdown.index('OpenCode Go'), markdown.index('OpenRouter')]
                    self.assertNotIn('## Rapport des LMM du catalogue général', markdown)
                    self.assertEqual(catalog['report_order'], ['opencode_go', 'openrouter'])
                    self.assertEqual(titles, sorted(titles))
                    headers = [line for line in markdown.splitlines() if line.startswith('| Rang |')]
                    self.assertEqual(len(headers), 2)
                    self.assertTrue(all(header.count('|') == 9 for header in headers))
                    self.assertIn('Coût moyen €/M', headers[1])
                    self.assertNotIn('clé None', markdown)

    def test_general_collection_failures_preserve_previous_reports(self):
        for path, module in self.modules():
            for failing in ('fetch_opencode_models', 'fetch_opencode_metadata', 'fetch_opencode_pricing'):
                with self.subTest(path=path, failing=failing):
                    with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                        output = Path(tmp)
                        for name in ('tfl.json', 'tfl.md'):
                            (output / name).write_text('previous-report', encoding='utf-8')
                        self.setup_main(module, output, stack)
                        stack.enter_context(patch.object(module, failing, side_effect=URLError('fixture')))
                        error = stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                        self.assertEqual(module.main(), 1)
                        self.assertIn('Erreur TFL', error.getvalue())
                        for name in ('tfl.json', 'tfl.md'):
                            self.assertEqual((output / name).read_text(), 'previous-report')

    def test_empty_selections_publish_all_catalogs_and_current_exclusions(self):
        fetches = {'opencode_go': 'fetch_models', 'opencode': 'fetch_opencode_models',
                   'openrouter': 'fetch_openrouter_models'}
        for path, module in self.modules():
            for empty_sections in (('opencode_go',), ('opencode',), ('openrouter',), tuple(fetches)):
                for cause in ('empty_api', 'missing_effort'):
                    with self.subTest(path=path, sections=empty_sections, cause=cause):
                        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                            output = Path(tmp)
                            for name in ('tfl.json', 'tfl.md'):
                                (output / name).write_text('previous-report', encoding='utf-8')
                            self.setup_main(module, output, stack)
                            for section in empty_sections:
                                fetch = getattr(module, fetches[section])
                                if cause == 'empty_api':
                                    fetch.return_value['data'] = []
                                else:
                                    for model in fetch.return_value['data']:
                                        model.pop('reasoning_capabilities')
                            stdout = stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                            self.assertEqual(module.main(), 0)
                            catalog = json.loads((output / 'tfl.json').read_text())
                            markdown = (output / 'tfl.md').read_text()
                            for section, fetch_name in fetches.items():
                                getattr(module, fetch_name).assert_called_once()
                                current = catalog[section]
                                self.assertEqual(current['selection_status'],
                                                 'empty' if section in empty_sections else 'available')
                                self.assertEqual(bool(current['models']), section not in empty_sections)
                                expected_excluded = int(section in empty_sections and cause == 'missing_effort')
                                self.assertEqual(current['excluded_model_count'], expected_excluded)
                                self.assertEqual(sum(current['exclusion_summary'].values()), expected_excluded)
                                if expected_excluded:
                                    self.assertEqual(current['excluded_models'][0]['exclusion_type'], 'reasoning_effort')
                                    self.assertNotIn(current['excluded_models'][0]['id'], markdown)
                            self.assertEqual(markdown.count('Aucun modèle admissible.'),
                                             sum(section != 'opencode' for section in empty_sections))
                            self.assertEqual(len([line for line in markdown.splitlines() if line.startswith('| Rang |')]), 2)
                            self.assertLess(markdown.index('OpenCode Go'), markdown.index('OpenRouter'))
                            self.assertNotIn('## Rapport des LMM du catalogue général', markdown)
                            self.assertIn('Taux BCE du ' + catalog['openrouter']['cost_exchange_rates']['date'], markdown)
                            self.assertIn(catalog['generated_at'], markdown)
                            self.assertIn(markdown, stdout.getvalue())
                            self.assertNotIn('previous-report', markdown)
                            self.assertNotIn('offline-fixture', markdown + json.dumps(catalog))
                            self.assertEqual(catalog['free_performance_results'], [])

    def test_pllm_can_read_published_catalogs_with_empty_sections(self):
        consumers = [ROOT / 'skills/pllm/scripts/evaluate.py', ROOT / 'plugins/pllm/skills/pllm/scripts/evaluate.py']
        fetches = {'opencode_go': 'fetch_models', 'opencode': 'fetch_opencode_models',
                   'openrouter': 'fetch_openrouter_models'}
        for (path, module), consumer_path in zip(self.modules(), consumers):
            for empty_sections in (('opencode_go',), ('opencode',), ('openrouter',), tuple(fetches)):
                with self.subTest(path=path, sections=empty_sections):
                    with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                        output = Path(tmp)
                        self.setup_main(module, output, stack)
                        # Prix exactement représentables pour isoler la lecture des sections vides.
                        module.fetch_openrouter_models.return_value['data'][0]['pricing'] = {
                            'prompt': '0.000000125', 'completion': '0.00000025'}
                        for section in empty_sections:
                            getattr(module, fetches[section]).return_value['data'] = []
                        stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                        self.assertEqual(module.main(), 0)
                        consumer = load_script(consumer_path)
                        catalog_path = output / 'tfl.json'
                        catalog = consumer.load_tfl_catalog(catalog_path)
                        for section in empty_sections:
                            self.assertEqual(catalog[section]['models'], [])
                        for mode in ('mode1', 'mode2', 'mode3', 'mode4', 'mode5'):
                            free = mode in ('mode3', 'mode4')
                            section = 'openrouter' if mode == 'mode5' else 'opencode_go'
                            with patch.object(consumer.performance, 'fetch_eur_rates',
                                              return_value=catalog['openrouter']['cost_exchange_rates']):
                                selected = consumer.candidates_for({'mode': mode, 'candidate_exclusions': []},
                                                                   'free' if free else 'paid', catalog_path)
                            expected = [] if free or section in empty_sections else [
                                'router-only' if section == 'openrouter' else 'go-only']
                            self.assertEqual([model['model_id'] for model in selected], expected)

    def test_existing_pllm_consumers_ignore_the_added_section(self):
        consumers = [ROOT / 'skills/pllm/scripts/evaluate.py', ROOT / 'plugins/pllm/skills/pllm/scripts/evaluate.py']
        for (path, module), consumer_path in zip(self.modules(), consumers):
            with self.subTest(path=path):
                with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                    output = Path(tmp)
                    self.setup_main(module, output, stack)
                    stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
                    self.assertEqual(module.main(), 0)
                    consumer = load_script(consumer_path)
                    selected, _ = consumer.tfl_opencode_model_at(1, output / 'tfl.json')
                    self.assertEqual(selected['id'], 'go-only')
                    loaded = consumer.load_tfl_catalog(output / 'tfl.json')
                    self.assertEqual(loaded['openrouter']['models'][0]['id'], 'router-only')


if __name__ == '__main__':
    unittest.main()
