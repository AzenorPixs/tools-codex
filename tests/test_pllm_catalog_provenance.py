"""Provenance des catalogues et isolation des refus, sans accès fournisseur."""

import io
import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from urllib.error import HTTPError

from test_extension_qualification import PLLM, load_script
import test_pllm_free_fallback as free_tests


class CatalogProvenanceTests(unittest.TestCase):
    workspace = free_tests.PllmFreeFallbackTests.workspace
    run_evaluation = free_tests.PllmFreeFallbackTests.run_evaluation

    def test_explicit_recent_catalog_wins_over_old_neighbor(self):
        for script in PLLM:
            with self.subTest(script=script):
                module, path, catalog = self.workspace(script)
                catalog['generated_at'] = '2026-01-01T10:00:00+01:00'
                path.write_text(json.dumps(catalog))
                neighbor = module.ROOT.parent / 'tfl/data/tfl.json'
                neighbor.parent.mkdir(parents=True)
                old = {'generated_at': '2001-01-01T00:00:00+00:00',
                       'opencode_go': {'models': [free_tests.row('old-paid')]},
                       'openrouter': {'models': []}}
                neighbor.write_text(json.dumps(old))
                data, events, output = self.run_evaluation(module, path)
                for index, identifier in ((2, 'free-go'), (3, 'free-go'), (5, 'free-router')):
                    model = data['models'][index]
                    self.assertEqual(model['model_id'], identifier)
                    self.assertEqual(model['state'], 'Valide')
                    self.assertEqual(model['catalog_source']['path'], str(path.resolve()))
                    self.assertEqual(model['catalog_source']['selection'], 'explicit')
                    self.assertEqual(model['catalog_source']['generated_at'], catalog['generated_at'])
                    self.assertEqual(model['catalog_selection']['category_candidates'], 1)
                    self.assertNotIn('resource_control', model)
                self.assertFalse(any(event[0] == 'quota' and event[1] in module.FREE_MODES for event in events))
                for line in output.splitlines():
                    if line.startswith('|'):
                        self.assertEqual(len(line.split('|')), 10)

    def test_empty_free_category_identifies_date_and_counts(self):
        for script in PLLM:
            module, path, catalog = self.workspace(script)
            catalog['generated_at'] = '2001-01-01T00:00:00+00:00'
            for section in ('opencode_go', 'openrouter'):
                catalog[section]['models'] = [r for r in catalog[section]['models'] if 'free' not in r['id']]
            path.write_text(json.dumps(catalog))
            data, events, _ = self.run_evaluation(module, path)
            for index in (2, 3, 5):
                model = data['models'][index]
                self.assertIn('dans ce catalogue (collecte : 01-01-01', model['cause'])
                self.assertEqual(model['performance_test']['status'], 'not_run')
                self.assertIsNone(model['ttft_seconds'])
                self.assertEqual(model['catalog_selection']['admissible_free'], 0)
                self.assertGreater(model['catalog_selection']['admissible_paid'], 0)
                self.assertEqual(model['catalog_source']['warnings'], [])
            self.assertFalse(any(event[0] == 'benchmark' and event[1] in module.FREE_MODES for event in events))

    def test_catalog_dates_never_invent_age_or_expiration(self):
        for script in PLLM:
            module = load_script(script)
            for payload, warning in (({}, 'missing_generated_at'),
                                     ({'generated_at': 'invalid-private-value'}, 'invalid_generated_at'),
                                     ({'generated_at': '2026-01-01T00:00:00'}, 'invalid_generated_at'),
                                     ({'generated_at': 123}, 'invalid_generated_at'),
                                     ({'generated_at': (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()},
                                      'future_generated_at')):
                result = module.catalog_provenance(payload)
                self.assertEqual(result['warnings'], [warning])
                self.assertIsNone(result['age_seconds'])
                self.assertNotIn('invalid-private-value', json.dumps(result))
            result = module.catalog_provenance({'generated_at': '2001-01-01T00:00:00+00:00'})
            self.assertEqual(result['selection'], 'default')
            self.assertEqual(result['warnings'], [])
            self.assertGreater(result['age_seconds'], 0)

    def test_mode2_resource_401_does_not_prevent_mode4(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            real_quota = module.quota

            def behavior(model, events):
                if model['mode'] == 'mode2':
                    payload = {'error': {'type': 'authentication_error', 'message': 'private-key private-account'}}
                    error = HTTPError('https://opencode.ai/zen/go/v1/usage', 401, 'private-reason', {},
                                      io.BytesIO(json.dumps(payload).encode()))
                    with patch.object(module, 'get', side_effect=error):
                        real_quota(model, 'private-key')
                return False

            data, events, output = self.run_evaluation(module, path, quota_behavior=behavior)
            failed = data['models'][1]
            self.assertEqual(failed['state'], 'Invalide')
            self.assertIn('Contrôle des quotas / solde : Authentification refusée', failed['cause'])
            self.assertEqual(failed['resource_control']['http_status'], 401)
            self.assertEqual(failed['resource_control']['endpoint'], 'https://opencode.ai/zen/go/v1/usage')
            self.assertEqual(failed['resource_control']['phase'], 'resource_control')
            self.assertEqual(failed['performance_test']['status'], 'not_run')
            self.assertEqual(data['models'][3]['state'], 'Valide')
            self.assertFalse(any(event[0] == 'benchmark' and event[1] == 'mode2' for event in events))
            for private in ('private-key', 'private-account', 'private-reason'):
                self.assertNotIn(private, json.dumps(data) + output)

    def test_visited_policies_drop_previous_resource_and_catalog_evidence(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, _, _ = self.run_evaluation(module, path)
            for model in data['models']:
                model['resource_control'] = {'status': 'failed', 'endpoint': 'obsolete'}
                model['catalog_source'] = {'path': 'obsolete'}
            (module.ROOT / 'data/pllm-current.json').write_text(json.dumps(data))
            refreshed, _, _ = self.run_evaluation(module, path)
            for model in refreshed['models']:
                self.assertNotIn('resource_control', model)
                self.assertNotIn('obsolete', json.dumps(model))


if __name__ == '__main__':
    unittest.main()
