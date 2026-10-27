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

    def test_high_or_xhigh_only_and_invalid_metadata_are_excluded(self):
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
                    with self.assertRaises(RuntimeError):
                        engine.reasoning({'provider': 'opencodego'}, 1024, metadata)

    def test_go_builder_reads_models_dev_medium_options_before_qualification(self):
        for script in TFL:
            module = load_script(script)
            payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
            payload['data'][0].pop('reasoning_capabilities', None)
            metadata['models']['new-model'].update(reasoning=True, reasoning_options=[
                {'type': 'effort', 'values': ['low', 'medium', 'high']}])
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertEqual(retained[0]['reasoning'], 'medium')
            self.assertEqual(retained[0]['reasoning_capabilities']['supported_efforts'], ['low', 'medium', 'high'])

            metadata['models']['new-model']['reasoning_options'] = [
                {'type': 'effort', 'values': ['high', 'xhigh']}]
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(retained, [])
            self.assertTrue(excluded)

    def test_go_builder_requires_medium_proof_for_free_and_paid(self):
        for script in TFL:
            module = load_script(script)
            payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
            metadata['models']['new-model'].pop('reasoning', None)
            payload['data'][0].pop('reasoning_capabilities', None)
            self.assertEqual(module.build_rows(payload, metadata, prices)[0], [])
            metadata['models']['new-model']['effort'] = {'supported_levels': ['medium']}
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertEqual(retained[0]['reasoning'], 'medium')

    def test_paid_and_free_ineligible_rows_never_reach_benchmark_or_tables(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                rows = [candidate('hidden-paid', section, False), candidate('hidden-free', section)]
                for item in rows:
                    item['reasoning_capabilities'] = {'supported_efforts': ['high', 'xhigh']}
                excluded, audit = [], []
                with patch.object(module.performance, 'benchmark', side_effect=AssertionError('Génération interdite')):
                    kept = module.qualify_free_models(rows, excluded, section, 'offline-key', audit)
                self.assertEqual(kept, [])
                self.assertEqual(len(excluded), 2)
                self.assertEqual(audit, [])
                report = (module.format_openrouter_table(rows, 'date') if section == 'openrouter'
                          else module.format_opencode_table(rows, 'mode1', 'date'))
                self.assertNotIn('hidden-', report)
                self.assertNotIn('hidden-', module.format_free_performance([
                    {'model_id': 'hidden-free', 'reasoning_capabilities': {'supported_efforts': ['high']}}]))

    def test_pllm_candidate_history_and_forcing_cannot_bypass_medium_proof(self):
        for script in PLLM:
            module = load_script(script)
            eligible = row('eligible')
            eligible['reasoning_capabilities'] = {'supported_efforts': ['medium', 'high']}
            admitted = module.catalog_candidate(eligible, 'opencode_go', 1, 'date')
            self.assertEqual(admitted['reasoning'], 'medium')
            stale = {**admitted, 'reasoning': 'high', 'requested_reasoning': 'high',
                     'performance_test': {'reasoning_request': {'reasoning_effort': 'high'}}}
            self.assertFalse(module.performance.effort_allowed(stale, require_recorded=True))
            self.assertFalse(module.performance.effort_allowed(
                {'reasoning_capabilities': {'supported_efforts': ['medium', 'high']}},
                require_recorded=True))
            hidden = copy.deepcopy(eligible)
            hidden.update(id='hidden', reasoning_capabilities={'supported_efforts': ['high', 'xhigh']})
            with self.assertRaisesRegex(RuntimeError, 'Medium'):
                module.catalog_candidate(hidden, 'opencode_go', 1, 'date')
            with patch.object(module, 'load_tfl_catalog', return_value={'opencode_go': {'models': [hidden, eligible]}}):
                model = {'mode': 'mode1', 'candidate_exclusions': []}
                with self.assertRaisesRegex(RuntimeError, 'forcé non admissible'):
                    module.candidates_for(model, 'paid', None, forced={'rank': 1})
                self.assertEqual(module.candidates_for(model, 'paid', None)[0]['model_id'], 'eligible')
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
            with self.assertRaisesRegex(RuntimeError, 'Medium'):
                module.candidates_for({'mode': 'mode6'}, 'paid', None)


if __name__ == '__main__':
    unittest.main()
