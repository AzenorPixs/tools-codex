"""Benchmark payant mode5, contrôles et continuité, sans fournisseur réel."""

import copy
import json
import unittest

from test_extension_qualification import PLLM
import test_pllm_free_fallback as fixtures
from test_pllm_free_fallback import row, http_error


class Mode5BenchmarkTests(unittest.TestCase):
    workspace = fixtures.PllmFreeFallbackTests.workspace
    run_evaluation = fixtures.PllmFreeFallbackTests.run_evaluation

    def paid_pair(self, script):
        module, path, catalog = self.workspace(script)
        cheap = row('cheap-router', 'openrouter')
        expensive = row('expensive-router', 'openrouter')
        expensive.update(input_price=0.11, output_price=0.11)
        catalog['openrouter']['models'] = [expensive, cheap]
        path.write_text(json.dumps(catalog))
        return module, path

    def test_strict_paid_thresholds_and_all_failed_candidates(self):
        for script in PLLM:
            for ttft, throughput, expected in ((89.999, 15.001, 'Valide'),
                                                (90, 16, 'Invalide'), (1, 15, 'Invalide')):
                with self.subTest(script=script, ttft=ttft, throughput=throughput):
                    module, path = self.paid_pair(script)

                    def behavior(model, budget):
                        model.update(ttft_seconds=ttft, tokens_per_second=throughput)
                        return True

                    data, events, _ = self.run_evaluation(module, path, benchmark_behavior=behavior,
                                                          forced={'mode': 'mode5'})
                    current = data['models'][4]
                    self.assertEqual(current['state'], expected)
                    self.assertEqual(current['throughput_scope'], 'response_only')
                    self.assertEqual(current['reasoning'], 'medium')
                    self.assertEqual(current['performance_criteria'],
                                     {'ttft_lt_seconds': 90, 'tokens_per_second_gt': 15})
                    self.assertEqual([e[3] for e in events if e[0] == 'benchmark'],
                                     [1024] if expected == 'Valide' else list(module.BUDGETS))

    def test_http_400_429_try_next_paid_with_fresh_budget(self):
        for script in PLLM:
            for code in (400, 429):
                module, path = self.paid_pair(script)

                def behavior(model, budget):
                    if model['model_id'] == 'cheap-router':
                        raise http_error(code)
                    model.update(ttft_seconds=1, tokens_per_second=25)
                    return True

                data, events, _ = self.run_evaluation(module, path, benchmark_behavior=behavior)
                current = data['models'][4]
                self.assertEqual(current['model_id'], 'expensive-router')
                self.assertEqual(current['state'], 'Valide')
                self.assertEqual([(e[2], e[3]) for e in events if e[:2] == ('benchmark', 'mode5')],
                                 [('cheap-router', 1024), ('expensive-router', 1024)])
                failed = current['candidate_results'][0]
                self.assertEqual(failed['performance_test']['attempts'][0]['http_error']['http_status'], code)

    def test_authentication_failure_stops_mode_without_next_candidate(self):
        for script in PLLM:
            module, path = self.paid_pair(script)

            def denied(model, budget):
                raise http_error(401)

            data, events, _ = self.run_evaluation(module, path, benchmark_behavior=denied)
            self.assertEqual(data['models'][4]['state'], 'Invalide')
            self.assertEqual([e[2] for e in events if e[:2] == ('benchmark', 'mode5')], ['cheap-router'])

    def test_credit_exhausted_between_tiers_stops_all_paid_candidates(self):
        for script in PLLM:
            module, path = self.paid_pair(script)

            def depleted(model, events):
                return model['mode'] == 'mode5' and sum(e[:2] == ('quota', 'mode5') for e in events) >= 3

            def incomplete(model, budget):
                return False

            data, events, _ = self.run_evaluation(module, path, quota_behavior=depleted,
                                                  benchmark_behavior=incomplete)
            self.assertEqual(data['models'][4]['state'], 'Invalide')
            self.assertEqual([(e[2], e[3]) for e in events if e[:2] == ('benchmark', 'mode5')],
                             [('cheap-router', 1024)])

    def test_forced_failed_rank_never_substitutes_and_truncation_is_inconclusive(self):
        for script in PLLM:
            module, path = self.paid_pair(script)
            data, events, _ = self.run_evaluation(module, path, benchmark_behavior=lambda m, b: False,
                                                  forced={'mode': 'mode5', 'rank': 1})
            current = data['models'][4]
            self.assertEqual(current['state'], 'Invalide')
            self.assertIn('Budget du test épuisé', current['cause'])
            self.assertEqual([(e[2], e[3]) for e in events if e[0] == 'benchmark'],
                             [('expensive-router', b) for b in module.BUDGETS])
            self.assertIsNone(data['selected_mode'])

    def test_success_memory_is_reused_only_for_same_medium_identity(self):
        for script in PLLM:
            module, path = self.paid_pair(script)

            def behavior(model, budget):
                model.update(ttft_seconds=1, tokens_per_second=25)
                return budget >= 2048

            data, events, _ = self.run_evaluation(module, path, benchmark_behavior=behavior,
                                                  forced={'mode': 'mode5', 'rank': 2})
            self.assertEqual(data['models'][4]['last_successful_max_tokens'], 2048)
            data, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode5', 'rank': 2})
            self.assertEqual([e[3] for e in events if e[0] == 'benchmark'], [2048])
            data, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode5', 'rank': 1})
            self.assertEqual([e[3] for e in events if e[0] == 'benchmark'], [1024])

    def test_unbenchmarked_history_is_invalidated_without_rewriting_on_load(self):
        for script in PLLM:
            module, path = self.paid_pair(script)
            data = module.load_current()
            old = data['models'][4]
            old.update(model_id='cheap-router', model='cheap-router', state='Valide', reasoning='medium', reasoning_capabilities={'supported_efforts': ['medium']},
                       selected=True, performance_test={'status': 'not_required'})
            old['candidate_results'] = [copy.deepcopy(old)]
            data.update(selected_mode='mode5', selection_status='selected')
            current = module.ROOT / 'data/pllm-current.json'
            current.parent.mkdir()
            raw = json.dumps(data).encode()
            current.write_bytes(raw)
            loaded = module.load_current()
            self.assertEqual(current.read_bytes(), raw)
            module.sanitize_reasoning_history(loaded)
            self.assertEqual(loaded['models'][4]['state'], 'Invalide')
            self.assertEqual(loaded['models'][4]['candidate_results'], [])
            data, _, output = self.run_evaluation(module, path, active=True)
            self.assertEqual(output, '')
            self.assertEqual(data['selected_mode'], 'mode1')
            self.assertFalse(data['models'][4]['evaluated_this_run'])
            self.assertEqual(data['models'][4]['state'], 'Invalide')


if __name__ == '__main__':
    unittest.main()
