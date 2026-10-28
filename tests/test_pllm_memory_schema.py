"""Récupération bornée et persistance rechargeable de la mémoire PLLM."""
import copy
import json
import unittest
from unittest.mock import patch

from test_extension_qualification import PLLM
import test_pllm_free_fallback as free_tests


class PllmMemorySchemaTests(unittest.TestCase):
    workspace = free_tests.PllmFreeFallbackTests.workspace
    run_evaluation = free_tests.PllmFreeFallbackTests.run_evaluation

    def observed_memory(self, module):
        model = dict(mode='mode7', model_id='deepseek-v4-flash', provider='deepseek',
                     reasoning='medium', throughput_scope='response_only',
                     api_protocol='chat_completions',
                     api_endpoint='https://api.deepseek.com/chat/completions',
                     throughput_metric='request_average_v1', throughput_window='request_total',
                     measurement_protocol_version=8, ttft_seconds=2.0, tokens_per_second=40.0)
        record = dict(identity=module.identity(model), last_successful_max_tokens=1024,
                      succeeded_at='2026-10-28T12:00:00+01:00',
                      ttft_seconds=2.0, tokens_per_second=40.0)
        configurations = {json.dumps(record['identity'], sort_keys=True): dict(record)}
        return {'policies': {'mode7': {**record, 'configurations': configurations}}}, model

    def test_observed_memory_load_is_read_only_and_identity_scoped(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            value, model = self.observed_memory(module)
            raw = json.dumps(value).encode()
            module.MEMORY_PATH.parent.mkdir()
            module.MEMORY_PATH.write_bytes(raw)
            loaded = module.load_memory()
            self.assertEqual(loaded, {**value, 'schema_version': 3})
            self.assertEqual(module.MEMORY_PATH.read_bytes(), raw)
            self.assertEqual(module.budgets_for(model, loaded)[0], 1024)
            changed = {**model, 'reasoning': 'high'}
            self.assertEqual(module.budgets_for(changed, loaded), module.BUDGETS)
            self.assertIsNone(changed['last_successful_max_tokens'])

    def test_success_round_trip_and_repeated_writes_keep_all_policies(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            memory, model = self.observed_memory(module)
            module.remember_success(model, 2048, memory)
            self.assertEqual(memory['schema_version'], 3)
            self.assertEqual(module.load_memory(), memory)
            self.assertEqual(module.budgets_for(model, memory)[0], 2048)
            other = {**model, 'mode': 'mode1', 'provider': 'opencodego', 'model_id': 'fixture'}
            module.remember_success(other, 4096, memory)
            self.assertEqual(module.load_memory(), memory)
            self.assertEqual(set(memory['policies']), {'mode1', 'mode7'})
            self.assertEqual(memory['policies']['mode7']['last_successful_max_tokens'], 2048)

    def test_empty_unversioned_argument_writes_schema_three(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            _, model = self.observed_memory(module)
            memory = {'policies': {}}
            module.remember_success(model, 1024, memory)
            self.assertEqual(module.load_memory(), memory)
            self.assertEqual(memory['schema_version'], 3)

    def test_invalid_and_ambiguous_inputs_preserve_disk_and_argument(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            observed, model = self.observed_memory(module)
            invalid = [[], {'policies': []}, {'policies': {'mode4': {}}},
                       {'policies': {'mode6': {}}}, {'schema_version': 9, 'policies': {}},
                       {'schema_version': True, 'policies': {}},
                       {**observed, 'extra': 'ambiguous'}]
            for field, value in (('identity', {}), ('last_successful_max_tokens', 8912),
                                 ('succeeded_at', 'invalid'), ('succeeded_at', '2026-10-28'),
                                 ('ttft_seconds', float('nan')), ('ttft_seconds', 90),
                                 ('tokens_per_second', 15), ('tokens_per_second', True),
                                 ('configurations', []), ('configurations', {})):
                item = copy.deepcopy(observed)
                item['policies']['mode7'][field] = value
                invalid.append(item)
            mismatch = copy.deepcopy(observed)
            configs = mismatch['policies']['mode7']['configurations']
            configs['wrong-key'] = configs.pop(next(iter(configs)))
            invalid.append(mismatch)
            incompatible = copy.deepcopy(observed)
            configs = incompatible['policies']['mode7']['configurations']
            next(iter(configs.values()))['identity']['reasoning'] = 'high'
            invalid.append(incompatible)
            module.MEMORY_PATH.parent.mkdir()
            for value in invalid:
                with self.subTest(script=script, value=value):
                    raw = json.dumps(value).encode()
                    module.MEMORY_PATH.write_bytes(raw)
                    with patch.object(module.subprocess, 'run') as lookup, self.assertRaisesRegex(RuntimeError, 'Mémoire'):
                        module.main(tfl_catalog=path)
                    lookup.assert_not_called()
                    self.assertEqual(module.MEMORY_PATH.read_bytes(), raw)
                    before = json.dumps(value)
                    with self.assertRaisesRegex(RuntimeError, 'Mémoire'):
                        module.remember_success(model, 1024, value)
                    self.assertEqual(json.dumps(value), before)
                    self.assertEqual(module.MEMORY_PATH.read_bytes(), raw)
            module.MEMORY_PATH.write_bytes(b'{invalid json')
            with self.assertRaisesRegex(RuntimeError, 'Mémoire'):
                module.load_memory()
            self.assertEqual(module.MEMORY_PATH.read_bytes(), b'{invalid json')

    def test_versioned_migrations_remain_reloadable(self):
        for script in PLLM:
            for version, old_mode in ((1, 'mode4'), (2, 'mode6'), (3, 'mode7')):
                module, _, _ = self.workspace(script)
                observed, model = self.observed_memory(module)
                memory = {'schema_version': version,
                          'policies': {old_mode: observed['policies']['mode7']}}
                module.remember_success(model, 2048, memory)
                self.assertEqual(set(memory['policies']), {'mode7'})
                self.assertEqual(memory['schema_version'], 3)
                self.assertEqual(module.load_memory(), memory)

    def test_main_recovers_observed_memory_and_publishes_current_evaluation(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            value, _ = self.observed_memory(module)
            module.MEMORY_PATH.parent.mkdir()
            module.MEMORY_PATH.write_text(json.dumps(value))
            data, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode7'})
            self.assertTrue(any(event[0] == 'benchmark' for event in events))
            self.assertEqual(data['selected_mode'], 'mode7')
            self.assertEqual(module.load_memory()['schema_version'], 3)
