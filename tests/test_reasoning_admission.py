"""Admission HIGH/XHIGH, y compris données anciennes, sans appel fournisseur."""
import copy
import unittest
from unittest.mock import patch

from test_extension_qualification import PLLM, TFL, load_script
from test_free_performance import candidate
from test_pllm_free_fallback import row
import test_tfl_go_metadata as go_fixtures


class ReasoningAdmissionTests(unittest.TestCase):
    def test_declared_levels_null_and_invalid_capabilities(self):
        for script in (*TFL, *PLLM):
            engine = load_script(script).performance
            for options, expected in (({'supported_efforts': ['high']}, 'high'),
                                      ({'supported_efforts': ['xhigh']}, 'xhigh'),
                                      ({'supported_efforts': None}, 'high')):
                model = {'provider': 'openrouter'}
                metadata = {'reasoning_capabilities': options}
                self.assertEqual(engine.verified_effort(metadata), expected)
                self.assertEqual(engine.reasoning(model, 1024, metadata), {'reasoning': {'effort': expected}})
            for options in ({}, {'supports_max_tokens': True}, {'supported_efforts': []},
                            {'supported_efforts': ['medium']}, {'supported_efforts': True},
                            {'supported_efforts': ['high', 1]}):
                with self.subTest(script=script, options=options):
                    metadata = {'reasoning_capabilities': options}
                    self.assertFalse(engine.effort_allowed(metadata))
                    with self.assertRaises(RuntimeError):
                        engine.reasoning({'provider': 'opencodego'}, 1024, metadata)

    def test_go_builder_requires_proof_for_free_and_paid(self):
        for script in TFL:
            module = load_script(script)
            payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
            metadata['models']['new-model'].pop('reasoning', None)
            payload['data'][0].pop('reasoning_capabilities', None)
            self.assertEqual(module.build_rows(payload, metadata, prices)[0], [])
            metadata['models']['new-model']['effort'] = {'supported_levels': ['xhigh']}
            retained, excluded = module.build_rows(payload, metadata, prices)
            self.assertEqual(excluded, [])
            self.assertEqual(retained[0]['reasoning'], 'xhigh')

    def test_paid_and_free_ineligible_rows_never_reach_benchmark_or_tables(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                rows = [candidate('hidden-paid', section, False), candidate('hidden-free', section)]
                for item in rows:
                    item['reasoning_capabilities'] = {}
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
                    {'model_id': 'hidden-free', 'reasoning_capabilities': {}}]))

    def test_pllm_candidate_history_and_forcing_cannot_bypass_proof(self):
        for script in PLLM:
            module = load_script(script)
            eligible = row('eligible')
            eligible['reasoning_capabilities'] = {'supported_efforts': ['high']}
            admitted = module.catalog_candidate(eligible, 'opencode_go', 1, 'date')
            self.assertEqual(admitted['reasoning'], 'high')
            hidden = copy.deepcopy(eligible)
            hidden.update(id='hidden', reasoning_capabilities={})
            with self.assertRaisesRegex(RuntimeError, 'HIGH/XHIGH'):
                module.catalog_candidate(hidden, 'opencode_go', 1, 'date')
            with patch.object(module, 'load_tfl_catalog', return_value={'opencode_go': {'models': [hidden, eligible]}}):
                model = {'mode': 'mode1', 'candidate_exclusions': []}
                with self.assertRaisesRegex(RuntimeError, 'forcé non admissible'):
                    module.candidates_for(model, 'paid', None, forced={'rank': 1})
                self.assertEqual(module.candidates_for(model, 'paid', None)[0]['model_id'], 'eligible')
            historical = {**module.initial_model(1, 'opencodego'), 'model_id': 'hidden',
                          'model': 'hidden', 'state': 'Valide', 'selected': True,
                          'candidate_results': [{'model_id': 'hidden', 'state': 'Valide'}]}
            self.assertNotIn('hidden', module.policy_table([historical]))
            data = {'models': [historical]}
            module.sanitize_reasoning_history(data)
            self.assertFalse(historical['selected'])
            self.assertEqual(historical['candidate_results'], [])
            self.assertEqual(historical['candidate_exclusions'][0]['model_id'], 'hidden')
            self.assertNotIn('hidden', module.policy_table(data['models']))

    def test_deepseek_direct_has_no_implicit_effort_proof(self):
        for script in PLLM:
            module = load_script(script)
            with self.assertRaisesRegex(RuntimeError, 'HIGH/XHIGH'):
                module.candidates_for({'mode': 'mode6'}, 'paid', None)


if __name__ == '__main__':
    unittest.main()
