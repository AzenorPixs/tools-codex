"""Admission Medium, y compris données anciennes, sans appel fournisseur."""
import copy
import unittest
from unittest.mock import patch

from test_extension_qualification import PLLM, TFL, load_script
from test_free_performance import candidate
from test_pllm_free_fallback import row
import test_tfl_go_metadata as go_fixtures


class ReasoningAdmissionTests(unittest.TestCase):
    def test_models_dev_medium_levels_drive_each_transport(self):
        declarations = (
            ('deepseek-v4.1-flash', ['low', 'medium', 'high', 'max']),
            ('muse-spark-1.3-contributor', ['minimal', 'low', 'medium', 'high', 'xhigh']),
            ('glm-5.3-flash', ['low', 'medium', 'high', 'max']),
            ('gpt-6-luna', ['none', 'low', 'medium', 'high', 'xhigh', 'max']),
            ('minimax-m3.1-flash', ['low', 'medium', 'high', 'xhigh', 'max']),
            ('beam-free', ['low', 'medium', 'high', 'xhigh', 'max']),
        )
        for script in (*TFL, *PLLM):
            engine = load_script(script).performance
            for model_id, levels in declarations:
                with self.subTest(script=script, model=model_id):
                    metadata = {'reasoning': True, 'reasoning_options': [
                        {'type': 'toggle'}, {'type': 'effort', 'values': levels},
                        {'type': 'budget_tokens'}]}
                    self.assertEqual(engine.verified_effort(metadata), 'medium')
                    for provider, protocol, parameters in (
                        ('opencodego', 'chat_completions', {'reasoning_effort': 'medium'}),
                        ('opencodego', 'responses', {'reasoning': {'effort': 'medium'}}),
                        ('opencodego', 'messages', {'thinking': {'type': 'adaptive'},
                                                   'output_config': {'effort': 'medium'}}),
                    ):
                        model = {'provider': provider, 'api_protocol': protocol}
                        self.assertEqual(engine.reasoning(model, 1024, metadata), parameters)
                        self.assertEqual(model['reasoning'], 'medium')

    def test_effort_metadata_does_not_prevent_testing_medium_parameter(self):
        invalid = (None, True, {}, [], [{'type': 'toggle'}], [{'type': 'budget_tokens'}],
                   [{'type': 'effort'}], [{'type': 'effort', 'values': None}],
                   [{'type': 'effort', 'values': 'medium'}],
                   [{'type': 'effort', 'values': ['medium', None]}],
                   [{'type': 'effort', 'values': ['high']}],
                   [{'type': 'effort', 'values': ['xhigh']}],
                   [{'type': 'effort', 'values': ['high', 'xhigh']}],
                   [{'type': 'effort', 'values': ['max']}],
                   [{'type': 'effort', 'values': ['medium']},
                    {'type': 'effort', 'values': ['low']}])
        for script in (*TFL, *PLLM):
            engine = load_script(script).performance
            for options in invalid:
                with self.subTest(script=script, options=options):
                    metadata = {'reasoning': True, 'reasoning_options': options}
                    self.assertFalse(engine.effort_allowed(metadata))
                    model = {'provider': 'opencodego', 'api_protocol': 'chat_completions'}
                    self.assertEqual(engine.reasoning(model, 1024, metadata),
                                     {'reasoning_effort': 'medium'})
            for levels in (['high'], ['xhigh'], ['high', 'xhigh'], ['low'], []):
                self.assertFalse(engine.effort_allowed(
                    {'reasoning_capabilities': {'supported_efforts': levels}}))

    def test_declared_medium_and_null_capabilities(self):
        for script in (*TFL, *PLLM):
            engine = load_script(script).performance
            for options in ({'supported_efforts': ['medium']}, {'supported_efforts': None}):
                model = {'provider': 'openrouter'}
                metadata = {'reasoning_capabilities': options}
                self.assertEqual(engine.verified_effort(metadata), 'medium')
                self.assertEqual(engine.reasoning(model, 1024, metadata),
                                 {'reasoning': {'effort': 'medium'}})
            for options in ({}, {'supports_max_tokens': True}, {'supported_efforts': []},
                            {'supported_efforts': ['high']}, {'supported_efforts': True},
                            {'supported_efforts': ['medium', 1]}):
                with self.subTest(script=script, options=options):
                    metadata = {'reasoning_capabilities': options}
                    self.assertFalse(engine.effort_allowed(metadata))
                    self.assertEqual(engine.reasoning(
                        {'provider': 'opencodego', 'api_protocol': 'responses'}, 1024, metadata),
                        {'reasoning': {'effort': 'medium'}})

    def test_go_builder_preserves_models_dev_effort_capabilities_for_later_testing(self):
        for script in TFL:
            module = load_script(script)
            payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
            payload['data'][0].pop('reasoning_capabilities', None)
            metadata['models']['new-model'].update(reasoning=True, reasoning_options=[
                {'type': 'effort', 'values': ['low', 'medium', 'high']}])
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertIsNone(retained[0]['reasoning'])
            self.assertEqual(retained[0]['reasoning_capabilities']['supported_efforts'], ['low', 'medium', 'high'])

            metadata['models']['new-model']['reasoning_options'] = [
                {'type': 'effort', 'values': ['high', 'xhigh']}]
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertEqual(retained[0]['reasoning_capabilities']['supported_efforts'], ['high', 'xhigh'])

    def test_go_builder_retains_unknown_effort_for_later_medium_request(self):
        for script in TFL:
            module = load_script(script)
            payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
            metadata['models']['new-model'].pop('reasoning', None)
            payload['data'][0].pop('reasoning_capabilities', None)
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertEqual(retained[0]['reasoning_capabilities'], {})
            self.assertIsNone(retained[0]['reasoning'])
            metadata['models']['new-model']['effort'] = {'supported_levels': ['medium']}
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertEqual(retained[0]['reasoning_capabilities']['supported_efforts'], ['medium'])

    def test_high_only_effort_metadata_is_proved_by_a_medium_benchmark(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                rows = [candidate('hidden-paid', section, False), candidate('hidden-free', section)]
                for item in rows:
                    item['reasoning_capabilities'] = {'supported_efforts': ['high', 'xhigh']}
                excluded, audit = [], []
                def successful_medium(model, key, budget, metadata, session_id=None):
                    acceptance = {'status': 'accepted', 'parameter': 'medium',
                                  'verified_by': 'completed_api_response'}
                    model.update(ttft_seconds=1, tokens_per_second=40,
                                 reasoning_acceptance=acceptance,
                                 performance_test={'status': 'completed',
                                                   'reasoning_acceptance': acceptance})
                    return True
                with patch.object(module.performance, 'benchmark', side_effect=successful_medium) as benchmark:
                    kept = module.qualify_free_models(rows, excluded, section, 'offline-key', audit)
                self.assertEqual([item['id'] for item in kept], ['hidden-paid', 'hidden-free'])
                self.assertEqual(excluded, [])
                self.assertEqual(len(audit), 1)
                self.assertEqual(audit[0]['reasoning_acceptance']['status'], 'accepted')
                benchmark.assert_called_once()
                self.assertEqual([item['id'] for item in rows], ['hidden-paid', 'hidden-free'])
                self.assertIn('hidden-free', module.format_free_performance(audit))

    def test_pllm_candidate_history_and_forcing_cannot_bypass_medium_proof(self):
        for script in PLLM:
            module = load_script(script)
            eligible = row('eligible')
            eligible['reasoning_capabilities'] = {'supported_efforts': ['medium', 'high']}
            admitted = module.catalog_candidate(eligible, 'opencode_go', 1, 'date')
            self.assertEqual(admitted['reasoning'], 'medium')
            legacy_override = {
                **admitted,
                'state': 'Valide',
                'selected': True,
                'user_override': {'model': 'qwen3.8-flash', 'reasoning': 'xhigh'},
                'performance_attempts': [{
                    'performance_test': {
                        'reasoning_request': {'output_config': {'effort': 'xhigh'}}
                    }
                }],
                'candidate_results': [{
                    **admitted,
                    'state': 'Valide',
                    'user_override': {'model': 'qwen3.8-flash', 'reasoning': 'xhigh'},
                    'performance_attempts': [{
                        'performance_test': {
                            'reasoning_request': {'output_config': {'effort': 'xhigh'}}
                        }
                    }],
                }],
                'candidate_exclusions': [],
            }
            self.assertTrue(module.performance.effort_allowed(legacy_override, require_recorded=True))
            module.sanitize_reasoning_history({'models': [legacy_override]})
            self.assertEqual(legacy_override['state'], 'Valide')
            self.assertTrue(legacy_override['selected'])
            self.assertEqual(len(legacy_override['candidate_results']), 1)
            stale = {**admitted, 'reasoning': 'high', 'requested_reasoning': 'high',
                     'performance_test': {'reasoning_request': {'reasoning_effort': 'high'}}}
            self.assertFalse(module.performance.effort_allowed(stale, require_recorded=True))
            self.assertFalse(module.performance.effort_allowed(
                {'reasoning_capabilities': {'supported_efforts': ['medium', 'high']}},
                require_recorded=True))
            hidden = copy.deepcopy(eligible)
            hidden.update(id='hidden', reasoning_capabilities={'supported_efforts': ['high', 'xhigh']})
            hidden_candidate = module.catalog_candidate(hidden, 'opencode_go', 1, 'date')
            self.assertEqual(hidden_candidate['reasoning'], 'medium')
            with patch.object(module, 'load_tfl_catalog', return_value={'opencode_go': {'models': [hidden, eligible]}}):
                model = {'mode': 'mode1', 'candidate_exclusions': []}
                forced = module.candidates_for(model, 'paid', None, forced={'rank': 1})
                self.assertEqual(forced[0]['model_id'], 'hidden')
                self.assertEqual(module.candidates_for(model, 'paid', None)[0]['model_id'], 'hidden')
            historical = {**module.initial_model(1, 'opencodego'), 'model_id': 'hidden',
                          'model': 'hidden', 'reasoning': 'high', 'requested_reasoning': 'high',
                          'reasoning_capabilities': {'supported_efforts': ['medium', 'high']},
                          'state': 'Valide', 'selected': True,
                          'candidate_results': [{'model_id': 'hidden', 'reasoning': 'medium',
                              'reasoning_capabilities': {'supported_efforts': ['medium', 'high']},
                              'performance_test': {'attempts': [
                                  {'reasoning_request': {'reasoning_effort': 'high'}}]},
                              'state': 'Valide'}]}
            self.assertNotIn('hidden', module.policy_table([historical]))
            data = {'models': [historical]}
            module.sanitize_reasoning_history(data)
            self.assertFalse(historical['selected'])
            self.assertEqual(historical['candidate_results'], [])
            self.assertEqual(historical['candidate_exclusions'][0]['model_id'], 'hidden')
            self.assertNotIn('hidden', module.policy_table(data['models']))

    def test_deepseek_direct_requires_medium_proof(self):
        for script in PLLM:
            module = load_script(script)
            unsupported = {'provider': 'deepseek', 'model_id': 'deepseek-v4-flash',
                           'field': 'reasoning', 'protocol': 'chat_completions',
                           'status': 'unsupported', 'conclusion': 'DeepSeek mappe medium à high.'}
            with patch.object(module.evidence_module.EvidenceResolver, 'resolve',
                              return_value=unsupported):
                candidate = module.candidates_for({'mode': 'mode7'}, 'paid', None)[0]
            self.assertEqual(candidate['model_id'], 'deepseek-v4-flash')
            self.assertEqual(candidate['model_investigations'][0]['status'], 'unsupported')


if __name__ == '__main__':
    unittest.main()
