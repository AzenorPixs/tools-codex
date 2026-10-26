"""Six politiques PLLM : contrats observables, migrations et seuils stricts."""

import copy
import json
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_extension_qualification import PLLM
import test_pllm_free_fallback as free_tests
from test_pllm_free_fallback import row, http_error


class PllmSixModesTests(unittest.TestCase):
    workspace = free_tests.PllmFreeFallbackTests.workspace
    run_evaluation = free_tests.PllmFreeFallbackTests.run_evaluation

    def test_free_limits_are_strict_and_paid_limits_preserved(self):
        for script in PLLM:
            for mode in ('mode3', 'mode4'):
                for ttft, throughput, expected in ((29.999, 20.001, 'Valide'),
                                                    (30, 21, 'Invalide'),
                                                    (30.001, 21, 'Invalide'),
                                                    (1, 20, 'Invalide'),
                                                    (1, 19.999, 'Invalide'),
                                                    (70.4, 25, 'Invalide')):
                    with self.subTest(script=script, mode=mode, ttft=ttft, throughput=throughput):
                        module, path, _ = self.workspace(script)

                        def behavior(model, budget):
                            model.update(ttft_seconds=ttft, tokens_per_second=throughput)
                            return True

                        data, events, _ = self.run_evaluation(module, path, benchmark_behavior=behavior,
                                                              forced={'mode': mode})
                        model = data['models'][int(mode[-1]) - 1]
                        self.assertEqual(model['state'], expected)
                        self.assertEqual(model['performance_criteria'],
                                         {'ttft_lt_seconds': 30, 'tokens_per_second_gt': 20})
                        self.assertFalse(any(event[0] == 'quota' for event in events))
                        attempts = model['performance_test']['attempts']
                        self.assertEqual([attempt['max_tokens'] for attempt in attempts],
                                         [1024] if expected == 'Valide' else list(module.BUDGETS))
                        self.assertEqual(module.MEMORY_PATH.exists(), expected == 'Valide')
            module, path, _ = self.workspace(script)
            data, _, _ = self.run_evaluation(module, path)
            for model in (data['models'][i] for i in (0, 1, 4, 5)):
                self.assertEqual(model['performance_criteria'],
                                 {'ttft_lt_seconds': 90, 'tokens_per_second_gt': 15})

    def test_free_modes_ignore_unavailable_quota_and_never_call_usage(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def unavailable(model, events):
                raise RuntimeError('Quota inaccessible')

            data, events, _ = self.run_evaluation(module, path, quota_behavior=unavailable)
            self.assertEqual(data['selected_mode'], 'mode3')
            for model in data['models'][2:4]:
                self.assertEqual(model['state'], 'Valide')
                self.assertIsNone(model['quotas'])
                self.assertEqual(model['quota_status'], 'not_applicable')
            self.assertTrue(all(event[1] not in ('mode3', 'mode4') for event in events if event[0] == 'quota'))
            for mode in ('mode3', 'mode4'):
                with patch.object(module, 'get') as get:
                    module.quota({'mode': mode}, 'offline-fixture')
                get.assert_not_called()

    def test_secrets_use_original_accounts_and_policy_attributes(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            lookups = []

            def lookup(args, **kwargs):
                self.assertEqual(args[:2], ['secret-tool', 'lookup'])
                attributes = dict(zip(args[2::2], args[3::2]))
                lookups.append(attributes)
                return SimpleNamespace(returncode=0, stdout=b'offline-fixture')

            data, _, output = self.run_evaluation(module, path, secret_lookup=lookup)
            self.assertEqual([item['policy'] for item in lookups],
                             ['mode1', 'mode2', 'mode1', 'mode2', 'mode3', 'mode4'])
            self.assertEqual(lookups[0], lookups[2])
            self.assertEqual(lookups[1], lookups[3])
            self.assertEqual(lookups[4]['account'], module.ACCOUNTS[2])
            self.assertEqual(lookups[5]['account'], module.ACCOUNTS[3])
            self.assertNotIn('offline-fixture', output + json.dumps(data))

    def test_active_stops_after_first_free_success_and_normal_evaluates_six(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, events, output = self.run_evaluation(module, path, exhausted=True, active=True)
            self.assertEqual(data['selected_mode'], 'mode3')
            self.assertEqual(output, '')
            self.assertTrue(all(not model['evaluated_this_run'] for model in data['models'][3:]))
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'],
                             ['free-go'])
            data, _, output = self.run_evaluation(module, path)
            self.assertTrue(all(model['evaluated_this_run'] for model in data['models']))
            self.assertEqual(sum(line.startswith('| mode') for line in output.splitlines()), 6)
            self.assertIn('mode3 : Non applicable', output)
            self.assertIn('mode4 : Non applicable', output)

    def test_free_modes_never_accept_paid_or_sub_context_candidates(self):
        for script in PLLM:
            module, path, catalog = self.workspace(script)
            short = row('short-free', free=True)
            short['context_length'] = 999_999
            catalog['opencode_go']['models'] = [short, row('looks-free-but-paid')]
            catalog['opencode']['models'] = []
            path.write_text(json.dumps(catalog))
            for mode in ('mode3', 'mode4'):
                data, events, _ = self.run_evaluation(module, path, forced={'mode': mode})
                model = data['models'][int(mode[-1]) - 1]
                self.assertEqual(model['state'], 'Invalide')
                self.assertFalse(any(event[0] == 'benchmark' for event in events))
                self.assertIn('Contexte TFL', model['candidate_exclusions'][0]['cause'])

    def test_free_http_failures_remain_visible_without_quotas(self):
        for script in PLLM:
            for mode in ('mode3', 'mode4'):
                for code in (400, 401, 403, 429):
                    module, path, _ = self.workspace(script)

                    def fail(model, budget):
                        raise http_error(code)

                    data, events, output = self.run_evaluation(module, path, benchmark_behavior=fail,
                                                              forced={'mode': mode})
                    self.assertIsNone(data['selected_mode'])
                    self.assertEqual(len(events), 1)
                    self.assertIn('HTTP ' + str(code), output)
                    self.assertIsNone(data['models'][int(mode[-1]) - 1]['quotas'])

    def legacy_current(self, module):
        data = module.load_current()
        data['models'] = [data['models'][i] for i in (0, 1, 4, 5)]
        for priority, model in enumerate(data['models'], 1):
            model.update(mode=f'mode{priority}', priority=priority, state='Valide',
                         selected=priority == 3, evaluated_this_run=True,
                         evaluated_at='2026-10-24T12:00:00+02:00',
                         model_id=f'old-{priority}', ttft_seconds=70.4, tokens_per_second=20)
        data.update(schema_version=1, selected_mode='mode3', selection_status='selected')
        return data

    def test_old_current_migration_preserves_file_and_prevents_stale_selection(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            old = self.legacy_current(module)
            current = module.ROOT / 'data/pllm-current.json'
            current.parent.mkdir()
            raw = json.dumps(old).encode()
            current.write_bytes(raw)
            migrated = module.load_current()
            self.assertEqual(current.read_bytes(), raw)
            self.assertEqual(migrated['schema_version'], 2)
            self.assertIsNone(migrated['selected_mode'])
            self.assertTrue(all(not m['selected'] and not m['evaluated_this_run'] for m in migrated['models']))
            self.assertEqual(migrated['models'][4]['model_id'], 'old-3')
            self.assertEqual(migrated['models'][5]['model_id'], 'old-4')
            self.assertTrue(all(m['ttft_seconds'] is None and m['state'] == 'Invalide'
                                for m in migrated['models'][2:4]))
            data, _, _ = self.run_evaluation(module, path, secret_ok=False, forced={'mode': 'mode3'})
            self.assertIsNone(data['selected_mode'])
            self.assertEqual(data['models'][4]['model_id'], 'old-3')
            self.assertFalse(data['models'][4]['evaluated_this_run'])

    def test_old_free_go_winner_cannot_remain_a_paid_winner(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            old = self.legacy_current(module)
            old['models'][0].update(provider='opencode', model_id='free-general', is_free=True)
            current = module.ROOT / 'data/pllm-current.json'
            current.parent.mkdir()
            current.write_text(json.dumps(old))
            data, events, _ = self.run_evaluation(module, path, exhausted=True, forced={'mode': 'mode1'})
            self.assertIsNone(data['selected_mode'])
            self.assertEqual(data['models'][0]['state'], 'Invalide')
            self.assertIsNone(data['models'][0]['ttft_seconds'])
            self.assertFalse(any(event[0] == 'benchmark' for event in events))

    def test_memory_remapping_does_not_seed_new_free_modes(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            old = {'schema_version': 1, 'policies': {f'mode{i}': {'last_successful_max_tokens': 8192,
                        'identity': {'model_id': f'old-{i}'}} for i in range(1, 5)}}
            module.MEMORY_PATH.parent.mkdir()
            raw = json.dumps(old).encode()
            module.MEMORY_PATH.write_bytes(raw)
            memory = module.load_memory()
            self.assertEqual(memory['schema_version'], 2)
            self.assertEqual(module.MEMORY_PATH.read_bytes(), raw)
            self.assertEqual(set(memory['policies']), {'mode1', 'mode2', 'mode5', 'mode6'})
            self.assertEqual(memory['policies']['mode5']['identity']['model_id'], 'old-3')
            for mode in ('mode3', 'mode4'):
                self.assertEqual(module.budgets_for({'mode': mode}, memory), module.BUDGETS)

    def test_invalid_memory_or_current_is_preserved_without_lookup(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            module.MEMORY_PATH.parent.mkdir()
            for value in ({'schema_version': 9, 'policies': {}}, [],
                          {'schema_version': 1, 'policies': {'mode5': {}}},
                          {'schema_version': 2, 'policies': {'mode3': []}}):
                raw = json.dumps(value).encode()
                module.MEMORY_PATH.write_bytes(raw)
                with patch.object(module.subprocess, 'run') as lookup, self.assertRaisesRegex(RuntimeError, 'Mémoire'):
                    module.main(tfl_catalog=path)
                lookup.assert_not_called()
                self.assertEqual(module.MEMORY_PATH.read_bytes(), raw)
            module.MEMORY_PATH.write_text(json.dumps({'schema_version': 2, 'policies': {}}))
            current = module.ROOT / 'data/pllm-current.json'
            pristine = module.load_current()
            for change in ('duplicate', 'provider', 'schema', 'priority'):
                data = copy.deepcopy(pristine)
                if change == 'duplicate':
                    data['models'][3] = copy.deepcopy(data['models'][2])
                elif change == 'provider':
                    data['models'][2]['provider'] = 'openrouter'
                elif change == 'schema':
                    data['schema_version'] = 3
                else:
                    data['models'][2]['priority'] = 4
                raw = json.dumps(data).encode()
                current.write_bytes(raw)
                with patch.object(module.subprocess, 'run') as lookup, self.assertRaisesRegex(RuntimeError, 'Historique'):
                    module.main(tfl_catalog=path)
                lookup.assert_not_called()
                self.assertEqual(current.read_bytes(), raw)

    def test_new_forced_commands_and_free_ranks(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            for command, expected in (('31', 'free-go'), ('32', 'free-general'),
                                      ('41', 'free-go'), ('42', 'free-general'),
                                      ('52', 'paid-router'), ('6', 'deepseek-v4-flash')):
                forced = module.FORCED_COMMANDS[command]
                data, events, _ = self.run_evaluation(module, path, forced=forced)
                selected = next(model for model in data['models'] if model['selected'])
                self.assertEqual(selected['mode'], forced['mode'])
                self.assertEqual(selected['model_id'], expected)
                self.assertEqual(sum(event[0] == 'benchmark' for event in events), 1)
            for command in ('33', '43', '51'):
                data, events, _ = self.run_evaluation(module, path, forced=module.FORCED_COMMANDS[command])
                self.assertIsNone(data['selected_mode'])
                self.assertFalse(any(event[0] == 'benchmark' for event in events))

    def test_free_color_marks_exact_rejection_limits_red(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            for mode in ('mode3', 'mode4'):
                self.assertEqual(module.performance_color('ttft', 30, mode), '🔴')
                self.assertEqual(module.performance_color('tokens', 20, mode), '🔴')
                self.assertNotEqual(module.performance_color('ttft', 29.999, mode), '🔴')
                self.assertNotEqual(module.performance_color('tokens', 20.001, mode), '🔴')

    def test_fixed_categories_cannot_be_overridden(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            for mode, category in (('mode1', 'free'), ('mode2', 'free'),
                                   ('mode3', 'paid'), ('mode4', 'paid'), ('mode5', 'free'), ('mode6', 'free')):
                with self.subTest(mode=mode), self.assertRaisesRegex(RuntimeError, 'Catégorie incompatible'):
                    module.candidates_for({'mode': mode, 'candidate_exclusions': []}, category, path)


if __name__ == '__main__':
    unittest.main()
