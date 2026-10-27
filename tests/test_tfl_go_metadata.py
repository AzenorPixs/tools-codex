"""Contrats de modalités et de transport Go, sans réseau ni génération."""

import copy
import io
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from test_tfl_pricing import SCRIPTS, document, load_script


ROOT = Path(__file__).resolve().parents[1]
API_DATE = '2026-10-25T01:00:00+02:00'
METADATA_DATE = '2026-10-25T01:00:01+02:00'


class GoMetadataTests(unittest.TestCase):
    def modules(self):
        return [(path, load_script(path)) for path in SCRIPTS]

    def fixture(self, module, model_id='new-model', sdk='@ai-sdk/openai-compatible'):
        payload = {'retrieved_at': API_DATE, 'data': [{'reasoning_capabilities': {'supported_efforts': ['high']}, 'id': model_id, 'context_length': 1_000_000}]}
        metadata = {'source': module.CONTEXT_METADATA_URL, 'retrieved_at': METADATA_DATE,
                    'provider': {'npm': sdk, 'api': 'https://opencode.ai/published-base/v9'},
                    'models': {model_id: {'reasoning': {'supported_efforts': ['high']}, 'limit': {'context': 1_000_000},
                                          'modalities': {'input': ['text', 'image', 'video'],
                                                         'output': ['text']}}}}
        pricing = {'source': module.SOURCE_URL, 'retrieved_at': METADATA_DATE,
                   'models': module.parse_go_pricing(document([(model_id, '$0.1', '$0.2', '-', '-')]))}
        return payload, metadata, pricing

    def test_unlisted_model_gets_published_modalities_transport_and_provenance(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = self.fixture(module)
                rows, excluded = module.build_rows(payload, metadata, pricing)
                self.assertEqual(excluded, [])
                row = rows[0]
                self.assertEqual(row['output_modalities'], ['text'])
                self.assertEqual(row['input_modalities'], ['image', 'text', 'video'])
                self.assertEqual(row['api_endpoint'], 'https://opencode.ai/published-base/v9/chat/completions')
                self.assertEqual(row['api_protocol'], 'chat_completions')
                self.assertEqual(row['endpoint_source'], 'models.dev')
                self.assertEqual(row['modalities_metadata']['output']['source'], 'models.dev')
                self.assertEqual(row['modalities_metadata']['output']['retrieved_at'], METADATA_DATE)
                self.assertEqual(row['routing_metadata']['retrieved_at'], METADATA_DATE)
                self.assertEqual(row['routing_status'], 'documented')
                self.assertFalse(row['routing_metadata']['generation_tested'])
                self.assertIsNone(row['routing_warning'])
                self.assertIn('Texte', module.format_opencode_table(rows, 'mode1', API_DATE))

    def test_minimax31_uses_compatible_metadata_without_family_inference(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = self.fixture(module, 'minimax-m3.1-flash')
                metadata['provider']['api'] = 'https://opencode.ai/inference/go/openai/v1'
                metadata['models']['minimax-m3.1-flash']['provider'] = {
                    'api': 'https://opencode.ai/inference/go/openai/v1'}
                row = module.build_rows(payload, metadata, pricing)[0][0]
                self.assertEqual(row['output_modalities'], ['text'])
                self.assertEqual(row['api_protocol'], 'chat_completions')
                self.assertEqual(row['api_endpoint'],
                                 'https://opencode.ai/inference/go/openai/v1/chat/completions')

    def test_sdk_contracts_and_model_override_select_protocol_without_model_names(self):
        contracts = [('@ai-sdk/openai-compatible', 'chat_completions', 'chat/completions'),
                     ('@ai-sdk/openai', 'responses', 'responses'),
                     ('@ai-sdk/anthropic', 'messages', 'messages')]
        for path, module in self.modules():
            for sdk, protocol, operation in contracts:
                with self.subTest(path=path, sdk=sdk):
                    payload, metadata, _ = self.fixture(module, 'any-unlisted-model', sdk)
                    route = module.go_transport(payload['data'][0], metadata, API_DATE)
                    self.assertEqual(route['api_protocol'], protocol)
                    self.assertTrue(route['api_endpoint'].endswith('/' + operation))
            payload, metadata, _ = self.fixture(module, 'gpt-6-luna')
            self.assertEqual(module.go_transport(payload['data'][0], metadata, API_DATE)['api_protocol'],
                             'chat_completions')
            metadata['models']['gpt-6-luna']['provider'] = {
                'npm': '@ai-sdk/anthropic', 'api': 'https://opencode.ai/changed-base/v8'}
            route = module.go_transport(payload['data'][0], metadata, API_DATE)
            self.assertEqual(route['api_endpoint'], 'https://opencode.ai/changed-base/v8/messages')
            self.assertEqual(route['routing_metadata']['sdk_scope'], 'model')

    def test_new_metadata_collection_changes_route_without_historical_fallback(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, _ = self.fixture(module)
                before = module.go_transport(payload['data'][0], metadata, API_DATE)
                metadata['provider'] = {'api': 'https://opencode.ai/next/v2', 'npm': '@ai-sdk/openai'}
                after = module.go_transport(payload['data'][0], metadata, API_DATE)
                self.assertNotEqual(before['api_endpoint'], after['api_endpoint'])
                self.assertEqual(after['api_endpoint'], 'https://opencode.ai/next/v2/responses')
                self.assertEqual(after['api_protocol'], 'responses')

    def test_explicit_api_route_has_its_own_source_and_timestamp(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, _ = self.fixture(module)
                model = payload['data'][0]
                model.update(api_endpoint='https://opencode.ai/api-published/v4/messages', api_protocol='messages')
                route = module.go_transport(model, metadata, API_DATE)
                self.assertEqual(route['api_endpoint'], model['api_endpoint'])
                self.assertEqual(route['endpoint_source'], 'opencode-go-api')
                self.assertEqual(route['routing_metadata']['retrieved_at'], API_DATE)
                model['api_protocol'] = 'responses'
                with self.assertRaisesRegex(RuntimeError, 'incompatible'):
                    module.go_transport(model, metadata, API_DATE)

    def test_partial_or_unknown_explicit_protocol_never_falls_back(self):
        for path, module in self.modules():
            for changes in ({'api_endpoint': 'https://opencode.ai/declared/messages'},
                            {'api_protocol': 'messages'},
                            {'api_endpoint': 'https://opencode.ai/declared/messages', 'api_protocol': 'unknown'}):
                with self.subTest(path=path, changes=changes):
                    payload, metadata, _ = self.fixture(module)
                    payload['data'][0].update(changes)
                    route = module.go_transport(payload['data'][0], metadata, API_DATE)
                    self.assertIsNone(route['api_endpoint'])
                    self.assertIsNone(route['api_protocol'])
                    self.assertTrue(route['routing_warning'])

    def test_missing_model_or_transport_stays_unknown_including_legacy_model_name(self):
        for path, module in self.modules():
            for kind in ('model', 'base', 'sdk', 'unknown-sdk'):
                with self.subTest(path=path, kind=kind):
                    payload, metadata, _ = self.fixture(module, 'qwen3.8-flash')
                    if kind == 'model':
                        metadata['models'] = {}
                    elif kind == 'base':
                        metadata['provider'].pop('api')
                    elif kind == 'sdk':
                        metadata['provider'].pop('npm')
                    else:
                        metadata['provider']['npm'] = '@unknown/transport'
                    route = module.go_transport(payload['data'][0], metadata, API_DATE)
                    self.assertIsNone(route['api_endpoint'])
                    self.assertTrue(route['routing_warning'])

    def test_unknown_declared_metadata_protocol_is_not_replaced_by_sdk_default(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, _ = self.fixture(module)
                metadata['models']['new-model']['provider'] = {'api_protocol': 'unsupported'}
                route = module.go_transport(payload['data'][0], metadata, API_DATE)
                self.assertIsNone(route['api_protocol'])
                self.assertTrue(route['routing_warning'])

    def test_unsafe_urls_are_rejected_without_echoing_the_url(self):
        urls = ['http://opencode.ai/v1', 'https://example.invalid/v1',
                'https://opencode.ai.example.invalid/v1', 'https://user:fixture@opencode.ai/v1',
                'https://opencode.ai:444/v1', 'https://opencode.ai:invalid/v1',
                'https://opencode.ai/v1?', 'https://opencode.ai/v1#',
                'https://opencode.ai/v1?secret=fixture', 'https://opencode.ai/\npath',
                'https://opencode.ai/\\path', '/relative/v1']
        for path, module in self.modules():
            for url in urls:
                with self.subTest(path=path, url=url):
                    payload, metadata, _ = self.fixture(module)
                    metadata['provider']['api'] = url
                    with self.assertRaises(RuntimeError) as error:
                        module.go_transport(payload['data'][0], metadata, API_DATE)
                    self.assertNotIn(url, str(error.exception))

    def test_default_https_port_and_new_base_are_accepted(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, _ = self.fixture(module)
                metadata['provider']['api'] = 'https://opencode.ai:443/new/published/base/'
                route = module.go_transport(payload['data'][0], metadata, API_DATE)
                self.assertEqual(route['api_endpoint'],
                                 'https://opencode.ai:443/new/published/base/chat/completions')

    def test_matching_api_modalities_take_api_provenance(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, _ = self.fixture(module)
                model = payload['data'][0]
                model.update(input_modalities=['video', 'IMAGE', 'text'], output_modalities=['TEXT'])
                resolved = module.go_modalities(model, metadata, API_DATE)
                self.assertEqual(resolved['output_modalities'], ['text'])
                self.assertEqual(resolved['modalities_metadata']['output']['source'], 'opencode-go-api')
                self.assertEqual(resolved['modalities_metadata']['output']['retrieved_at'], API_DATE)

    def test_contradictory_modalities_fail_between_and_inside_sources(self):
        for path, module in self.modules():
            for changes in ({'output_modalities': ['audio']}, {'input_modalities': ['text']},
                            {'output_modalities': ['text'], 'architecture': {'output_modalities': ['audio']}}):
                with self.subTest(path=path, changes=changes):
                    payload, metadata, _ = self.fixture(module)
                    payload['data'][0].update(changes)
                    with self.assertRaisesRegex(RuntimeError, 'contradictoires'):
                        module.go_modalities(payload['data'][0], metadata, API_DATE)

    def test_absent_or_invalid_modalities_do_not_invent_text(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = self.fixture(module, 'qwen3.8-flash')
                metadata['models']['qwen3.8-flash'].pop('modalities')
                row = module.build_rows(payload, metadata, pricing)[0][0]
                self.assertIsNone(row['output_modalities'])
                self.assertIn('Non vérifié', module.format_opencode_table([row], 'mode1', API_DATE))
                for value in ('text', [''], [True], {'text': True}):
                    invalid = copy.deepcopy(metadata)
                    invalid['models']['qwen3.8-flash']['modalities'] = {'output': value}
                    with self.assertRaisesRegex(RuntimeError, 'modalités'):
                        module.build_rows(payload, invalid, pricing)

    def test_nontext_output_filters_use_collected_modalities(self):
        for path, module in self.modules():
            for modality in ('audio', 'video', 'speech', 'sound'):
                with self.subTest(path=path, modality=modality):
                    payload, metadata, pricing = self.fixture(module)
                    metadata['models']['new-model']['modalities']['output'] = ['text', modality]
                    rows, excluded = module.build_rows(payload, metadata, pricing)
                    self.assertEqual(rows, [])
                    self.assertEqual(excluded[0]['output_modalities'], sorted(['text', modality]))
            payload, metadata, pricing = self.fixture(module)
            metadata['models']['new-model']['modalities']['output'] = ['image']
            row = module.build_rows(payload, metadata, pricing)[0][0]
            self.assertEqual(row['multimedia_status'], 'verified_output')
            self.assertIn('| image |', module.format_opencode_table([row], 'mode1', API_DATE))

    def test_fetch_metadata_preserves_provider_defaults_without_unrelated_fields(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                _, metadata, _ = self.fixture(module)
                raw = json.dumps({'opencode-go': {**metadata['provider'], 'models': metadata['models'],
                                                  'env': ['UNUSED_VARIABLE_NAME']}}).encode()
                with patch.object(module, 'urlopen', return_value=io.BytesIO(raw)):
                    collected = module.fetch_go_metadata(1)
                self.assertEqual(collected['provider'], metadata['provider'])
                self.assertEqual(collected['models'], metadata['models'])
                self.assertEqual(collected['source'], module.CONTEXT_METADATA_URL)
                self.assertTrue(collected['retrieved_at'])
                self.assertNotIn('UNUSED_VARIABLE_NAME', json.dumps(collected))

    def test_missing_api_context_uses_the_same_full_metadata_catalog(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                payload, metadata, pricing = self.fixture(module)
                payload['data'][0].pop('context_length')
                row = module.build_rows(payload, metadata, pricing)[0][0]
                self.assertEqual(row['context_length'], 1_000_000)
                self.assertEqual(row['context_source'], 'models.dev')

    def test_invalid_metadata_preserves_previous_reports(self):
        for path, module in self.modules():
            for error_kind in ('modalities', 'route'):
                with self.subTest(path=path, error_kind=error_kind):
                    payload, metadata, pricing = self.fixture(module)
                    if error_kind == 'modalities':
                        payload['data'][0]['output_modalities'] = ['audio']
                    else:
                        metadata['provider']['api'] = 'https://example.invalid/v1'
                    with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp, ExitStack() as stack:
                        output = Path(tmp)
                        for name in ('tfl.json', 'tfl.md'):
                            (output / name).write_text('previous-report', encoding='utf-8')
                        stack.enter_context(patch.dict(module.os.environ, {'CODEX_HOME': str(output / 'codex-profile')}, clear=True))
                        stack.enter_context(patch.object(module, 'parse_args', return_value=SimpleNamespace(
                            policy_option=None, policy='auto', timeout=1, output_dir=output)))
                        stack.enter_context(patch.object(module, 'urlopen', side_effect=AssertionError('réseau interdit')))
                        stack.enter_context(patch.object(module, 'select_secret', return_value=('mode1', 'offline-fixture')))
                        stack.enter_context(patch.object(module, 'fetch_models', return_value=payload))
                        stack.enter_context(patch.object(module, 'fetch_go_metadata', return_value=metadata))
                        stack.enter_context(patch.object(module, 'fetch_go_pricing', return_value=pricing))
                        error = stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                        self.assertEqual(module.main(), 1)
                        self.assertIn('Erreur TFL', error.getvalue())
                        self.assertNotIn('offline-fixture', error.getvalue())
                        for name in ('tfl.json', 'tfl.md'):
                            self.assertEqual((output / name).read_text(), 'previous-report')

    def test_generated_route_is_readable_by_unchanged_pllm_consumers(self):
        consumers = [ROOT / 'skills/pllm/scripts/evaluate.py',
                     ROOT / 'plugins/pllm/skills/pllm/scripts/evaluate.py']
        for (path, module), consumer_path in zip(self.modules(), consumers):
            with self.subTest(path=path):
                payload, metadata, pricing = self.fixture(module)
                rows, _ = module.build_rows(payload, metadata, pricing)
                consumer = load_script(consumer_path)
                with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp:
                    catalog = Path(tmp) / 'tfl.json'
                    catalog.write_text(json.dumps({'generated_at': METADATA_DATE,
                                                   'opencode_go': {'models': rows}}), encoding='utf-8')
                    selected, generated_at = consumer.tfl_opencode_model_at(1, catalog)
                    self.assertEqual(selected['api_endpoint'], rows[0]['api_endpoint'])
                    self.assertEqual(selected['api_protocol'], 'chat_completions')
                    self.assertEqual(generated_at, METADATA_DATE)


if __name__ == '__main__':
    unittest.main()
