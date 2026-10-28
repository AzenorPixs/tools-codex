"""Premier succès par prix payant ou ordre gratuit, sans accès réel."""

import json
import unittest

from test_extension_qualification import PLLM
import test_pllm_free_fallback as fallback
from test_pllm_free_fallback import row


class PllmPricePriorityTests(unittest.TestCase):
    workspace = fallback.PllmFreeFallbackTests.workspace
    run_evaluation = fallback.PllmFreeFallbackTests.run_evaluation

    def priced_catalog(self, script):
        module, path, catalog = self.workspace(script)
        for section in ('opencode_go', 'openrouter'):
            expensive = row('expensive', section)
            cheap = row('cheap', section)
            if section == 'openrouter':
                expensive.update(input_price=0.14, output_price=0.28)
                cheap.update(input_price=0.1, output_price=0.2)
            else:
                expensive['reference_pricing_usd_per_million_tokens'] = {
                    'input_off_peak': 0.14, 'output_off_peak': 0.28}
                cheap['reference_pricing_usd_per_million_tokens'] = {
                    'input_off_peak': 0.1, 'output_off_peak': 0.2}
            catalog[section]['models'] = [expensive, cheap]
        path.write_text(json.dumps(catalog))
        return module, path, catalog

    @staticmethod
    def speeds(model, budget):
        cheap = model['model_id'] == 'cheap'
        model.update(ttft_seconds=13 if cheap else 0.8,
                     tokens_per_second=113 if cheap else 200)
        return True

    def test_cheaper_valid_paid_stops_before_more_expensive_candidate(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, path, _ = self.priced_catalog(script)
                data, _, _ = self.run_evaluation(module, path, benchmark_behavior=self.speeds)
                for model in (data['models'][0], data['models'][1], data['models'][4]):
                    self.assertEqual(model['model_id'], 'cheap')
                    self.assertEqual(model['model_source']['rank'], 2)
                    self.assertTrue(all(c['state'] == 'Valide' for c in model['candidate_results']))
                    self.assertEqual([c['model_id'] for c in model['candidate_results']], ['cheap'])
                    self.assertEqual(model['model_source']['selector'], 'tfl_price_first_success')
                self.assertEqual(data['models'][4]['performance_test']['status'], 'not_required')
                self.assertIsNone(data['models'][4]['ttft_seconds'])
                self.assertEqual(data['selected_mode'], 'mode1')

    def test_cheapest_failing_performance_cannot_win(self):
        for script in PLLM:
            module, path, catalog = self.priced_catalog(script)
            for section in ('opencode_go', 'openrouter'):
                last = row('last', section)
                if section == 'openrouter':
                    last.update(input_price=0.3, output_price=0.4)
                else:
                    last['reference_pricing_usd_per_million_tokens'] = {
                        'input_off_peak': 0.3, 'output_off_peak': 0.4}
                catalog[section]['models'].extend([last, row('free', section, True)])
            path.write_text(json.dumps(catalog))

            def behavior(model, budget):
                model.update(ttft_seconds=1, tokens_per_second=10 if model['model_id'] == 'cheap' else 100)
                return True

            data, _, _ = self.run_evaluation(module, path, benchmark_behavior=behavior)
            for model in (data['models'][0], data['models'][1]):
                self.assertEqual(model['model_id'], 'expensive')
                cheap = next(c for c in model['candidate_results'] if c['model_id'] == 'cheap')
                self.assertEqual([c['model_id'] for c in model['candidate_results']], ['cheap', 'expensive'])
                self.assertEqual(cheap['state'], 'Invalide')
                self.assertEqual([a['max_tokens'] for a in cheap['performance_test']['attempts']],
                                 [1024, 2048, 4096, 8192])
            self.assertEqual(data['models'][4]['model_id'], 'cheap')
            self.assertEqual(data['models'][4]['performance_test']['status'], 'not_required')
            self.assertEqual(data['models'][4]['performance_test']['status'], 'not_required')

    def test_equal_prices_keep_catalog_order_without_binary_addition_bias(self):
        for script in PLLM:
            module, path, catalog = self.priced_catalog(script)
            for section in ('opencode_go', 'openrouter'):
                first, second = catalog[section]['models']
                if section == 'openrouter':
                    first.update(input_price=0.15, output_price=0.15)
                else:
                    first['reference_pricing_usd_per_million_tokens'] = {
                        'input_off_peak': 0.15, 'output_off_peak': 0.15}
            path.write_text(json.dumps(catalog))

            def behavior(model, budget):
                model.update(ttft_seconds=1, tokens_per_second=200 if model['model_id'] == 'cheap' else 100)
                return True

            data, _, _ = self.run_evaluation(module, path, benchmark_behavior=behavior)
            for model in (data['models'][0], data['models'][1], data['models'][4]):
                self.assertEqual(model['model_id'], 'expensive')
                self.assertAlmostEqual(model['candidate_results'][0]['average_price_usd_per_million_tokens'], 0.15)

    def test_equal_prices_stop_without_measuring_a_faster_candidate(self):
        for script in PLLM:
            for equal_ttft in (False, True):
                module, path, _ = self.workspace(script)

                def behavior(model, budget):
                    model.update(ttft_seconds=1 if equal_ttft or model['model_id'] == 'paid-b' else 2,
                                 tokens_per_second=100)
                    return True

                data, events, _ = self.run_evaluation(module, path, benchmark_behavior=behavior, active=True)
                self.assertEqual(data['models'][0]['model_id'], 'paid-a')
                self.assertEqual([e[2] for e in events if e[0] == 'benchmark'], ['paid-a'])

    def test_free_modes_keep_first_go_success_and_router_never_falls_back(self):
        for script in PLLM:
            module, path, catalog = self.workspace(script)
            catalog['opencode_go']['models'].append(row('fast-free-go', free=True))
            catalog['openrouter']['models'].append(row('fast-free-router', 'openrouter', True))
            path.write_text(json.dumps(catalog))

            def behavior(model, budget):
                model.update(ttft_seconds=1, tokens_per_second=80 if model['model_id'] in (
                    'free-general', 'fast-free-router', 'fast-free-go') else 30)
                return True

            data, events, _ = self.run_evaluation(module, path, exhausted=True, benchmark_behavior=behavior)
            self.assertEqual([m['model_id'] for m in data['models'][2:4]], ['free-go', 'free-go'])
            self.assertEqual(data['models'][4]['state'], 'Invalide')
            self.assertFalse(any(e[0] == 'benchmark' and e[1] == 'mode5' for e in events))
            self.assertTrue(all(len(m['candidate_results']) == 1 for m in data['models'][2:4]))
            self.assertFalse(any(e[0] == 'quota' and e[1] in ('mode3', 'mode4') for e in events))

    def test_paid_sub_million_context_is_excluded_before_generation(self):
        for script in PLLM:
            module, path, catalog = self.priced_catalog(script)
            for section in ('opencode_go', 'openrouter'):
                catalog[section]['models'][1]['context_length'] = 999_999
            path.write_text(json.dumps(catalog))
            data, events, _ = self.run_evaluation(module, path)
            for index in (0, 1):
                model = data['models'][index]
                self.assertEqual(model['model_id'], 'expensive')
                self.assertIn('Contexte TFL', model['candidate_exclusions'][0]['cause'])
                self.assertEqual([e[2] for e in events if e[0] == 'benchmark' and e[1] == model['mode']],
                                 ['expensive'])
            router = data['models'][4]
            self.assertEqual(router['model_id'], 'expensive')
            self.assertEqual(router['state'], 'Valide')
            self.assertIsNone(router['ttft_seconds'])
            self.assertFalse(any(e[0] == 'benchmark' and e[1] == 'mode5' for e in events))

    def test_paid_go_without_medium_metadata_is_tested_in_price_order(self):
        for script in PLLM:
            module, path, catalog = self.priced_catalog(script)
            catalog['opencode_go']['models'][1]['reasoning_capabilities'] = {'supported_efforts': ['low']}
            path.write_text(json.dumps(catalog))
            data, events, _ = self.run_evaluation(module, path)
            for model in data['models'][:2]:
                self.assertEqual(model['model_id'], 'cheap')
                self.assertEqual([c['model_id'] for c in model['candidate_results']], ['cheap'])
                self.assertEqual(model['candidate_exclusions'], [])
                self.assertEqual(model['candidate_results'][0]['reasoning_acceptance']['status'], 'accepted')
                self.assertEqual([e[2] for e in events if e[0] == 'benchmark' and e[1] == model['mode']],
                                 ['cheap'])

    def test_invalid_price_is_excluded_before_generation(self):
        for script in PLLM:
            module, path, catalog = self.priced_catalog(script)
            catalog['opencode_go']['models'][1]['reference_pricing_usd_per_million_tokens'].pop('input_off_peak')
            path.write_text(json.dumps(catalog))
            data, events, _ = self.run_evaluation(module, path, benchmark_behavior=self.speeds, active=True)
            self.assertEqual(data['models'][0]['model_id'], 'expensive')
            self.assertEqual(len(data['models'][0]['candidate_exclusions']), 1)
            self.assertEqual([e[2] for e in events if e[0] == 'benchmark'], ['expensive'])

    def test_active_stops_after_cheapest_success_and_forced_rank_stays_forced(self):
        for script in PLLM:
            module, path, _ = self.priced_catalog(script)
            data, events, output = self.run_evaluation(module, path, benchmark_behavior=self.speeds, active=True)
            self.assertEqual(data['models'][0]['model_id'], 'cheap')
            self.assertEqual([e[2] for e in events if e[0] == 'benchmark'], ['cheap'])
            self.assertTrue(all(e[1] == 'mode1' for e in events))
            self.assertEqual(output, '')
            data, events, _ = self.run_evaluation(module, path, benchmark_behavior=self.speeds,
                                                 forced={'mode': 'mode1', 'rank': 1})
            self.assertEqual(data['models'][0]['model_id'], 'expensive')
            self.assertEqual([e[2] for e in events if e[0] == 'benchmark'], ['expensive'])

    def test_stale_price_is_cleared_and_direct_deepseek_has_no_invented_price(self):
        for script in PLLM:
            module, path, _ = self.priced_catalog(script)
            data, _, _ = self.run_evaluation(module, path, benchmark_behavior=self.speeds)
            self.assertNotIn('average_price_usd_per_million_tokens', data['models'][5])
            data, _, _ = self.run_evaluation(module, path, exhausted=True)
            for model in data['models'][:2]:
                self.assertEqual(model['state'], 'Invalide')
                self.assertNotIn('average_price_usd_per_million_tokens', model)


if __name__ == '__main__':
    unittest.main()
