"""Preuves documentaires, périmètres et investigations ; aucun fournisseur réel."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from eur_fixtures import FX
from test_extension_qualification import ROOT, TFL, PLLM, load_script
import test_tfl_go_metadata as go_fixtures

BODY = b'Current official documentation'
DATE = '2026-10-26T14:00:00+01:00'


def record(provider='opencode_go', field='reasoning', status='verified', **changes):
    result = {'provider': provider, 'model_id': 'new-model', 'field': field,
              'protocol': 'chat_completions' if field == 'reasoning' else None,
              'status': status, 'investigated_at': DATE,
              'conclusion': 'Investigation des sources officielles terminée.',
              'sources': [{'url': 'https://official.example/docs', 'authority': 'official',
                           'sha256': hashlib.sha256(BODY).hexdigest(), 'retrieved_at': DATE}]}
    if status == 'verified':
        result['value'] = 1_000_000 if field == 'context' else {'supported_efforts': ['high', 'xhigh']}
    result.update(changes)
    return result


class ModelEvidenceTests(unittest.TestCase):
    def resolver(self, module, records, fetch=None):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as tmp:
            path = Path(tmp) / 'model-evidence.json'
            path.write_text(json.dumps({'schema_version': 1, 'records': records}))
            return module.evidence_module.EvidenceResolver([path], fetch=fetch or (lambda *_: BODY))

    def fixture(self, module, section):
        payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
        raw = payload['data'][0]
        raw.pop('context_length')
        raw.pop('reasoning_capabilities')
        metadata['models']['new-model'].update(limit={}, reasoning=True)
        if section == 'openrouter':
            raw['pricing'] = {'prompt': '0.0000001', 'completion': '0.0000001'}
            return payload, {}, lambda data: module.build_openrouter_rows(data, (), exchange_rates=FX)
        metadata['provider_id'] = section
        return payload, metadata, lambda data: module.build_rows(
            data, metadata, prices, general_catalog=section == 'opencode', blacklisted_models=())

    def test_context_then_effort_recovered_for_each_catalog_with_sources(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                with self.subTest(script=script, section=section):
                    payload, metadata, builder = self.fixture(module, section)
                    calls = []
                    def fetch(url, timeout):
                        calls.append(url)
                        return BODY
                    resolver = self.resolver(module, [record(section, 'context'), record(section)], fetch)
                    rows, excluded, findings = module.build_investigated(builder, payload, metadata, section, resolver)
                    self.assertEqual(excluded, [])
                    self.assertEqual(rows[0]['context_length'], 1_000_000)
                    self.assertEqual(rows[0]['context_source'], 'documented_investigation')
                    self.assertEqual(rows[0]['reasoning'], 'high')
                    self.assertEqual([f['status'] for f in findings], ['verified', 'verified'])
                    self.assertEqual(len(calls), 1)
                    self.assertNotIn('context_length', payload['data'][0])

    def test_completed_context_investigation_without_proof_excludes(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                payload, metadata, builder = self.fixture(module, section)
                resolver = self.resolver(module, [record(section, 'context', 'unverifiable')])
                rows, excluded, findings = module.build_investigated(builder, payload, metadata, section, resolver)
                self.assertEqual(rows, [])
                self.assertIn('contexte non vérifiable après investigation', excluded[0]['reason'])
                self.assertEqual(findings[0]['status'], 'unverifiable')

    def test_verified_short_context_does_not_lower_the_threshold(self):
        for script in TFL:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                payload, metadata, builder = self.fixture(module, section)
                resolver = self.resolver(module, [record(section, 'context', value=999_999)])
                rows, excluded, findings = module.build_investigated(builder, payload, metadata, section, resolver)
                self.assertEqual(rows, [])
                self.assertIn('contexte', excluded[0]['reason'])
                self.assertEqual(findings[0]['status'], 'verified')

    def test_lm_exclusion_precedes_metadata_and_investigation(self):
        for script in TFL:
            module = load_script(script)
            payload = {'data': [{'id': 'blocked'}]}
            resolver = module.evidence_module.EvidenceResolver()
            with patch.object(module, 'context_info', side_effect=AssertionError('Métadonnées interdites')), \
                 patch.object(resolver, 'resolve', side_effect=AssertionError('Recherche interdite')):
                rows, excluded, findings = module.build_investigated(
                    lambda data: ([], [{'id': 'blocked', 'reason': 'liste noire LM'}]),
                    payload, {}, 'opencode_go', resolver)
            self.assertEqual(rows, [])
            self.assertEqual(findings, [])

    def test_absent_changed_or_unreachable_source_requires_new_research(self):
        for script in TFL:
            module = load_script(script)
            resolvers = [self.resolver(module, []), self.resolver(module, [record()], lambda *_: b'changed')]
            def inaccessible(*_):
                raise OSError('offline')
            resolvers.append(self.resolver(module, [record()], inaccessible))
            for resolver in resolvers:
                result = resolver.resolve('opencode_go', 'new-model', 'reasoning', 'chat_completions')
                self.assertEqual(result['status'], 'required')
                self.assertNotIn('value', result)

    def test_provider_model_and_protocol_are_exact_without_cross_borrowing(self):
        for script in TFL:
            module = load_script(script)
            resolver = self.resolver(module, [record()])
            for args in (('opencode', 'new-model', 'reasoning', 'chat_completions'),
                         ('openrouter', 'new-model', 'reasoning', 'chat_completions'),
                         ('opencode_go', 'vendor/new-model', 'reasoning', 'chat_completions'),
                         ('opencode_go', 'new-model', 'reasoning', 'responses')):
                self.assertEqual(resolver.resolve(*args)['status'], 'required')

    def test_documented_thinking_equivalence_preserves_high_and_route(self):
        for script in (*TFL, *PLLM):
            module = load_script(script)
            metadata = {'reasoning_capabilities': {'supported_efforts': ['high', 'xhigh'],
                        'effort_equivalence': 'thinking_enabled', 'effort_protocol': 'chat_completions'}}
            model = {'provider': 'opencodego', 'api_protocol': 'chat_completions',
                     'api_endpoint': 'https://opencode.ai/published/chat/completions'}
            self.assertEqual(module.performance.reasoning(model, 1024, metadata), {'thinking': {'type': 'enabled'}})
            self.assertEqual(model['reasoning'], 'high')
            self.assertEqual(model['reasoning_semantics'], 'documented_equivalent')
            self.assertEqual(model['api_endpoint'], 'https://opencode.ai/published/chat/completions')
            with self.assertRaises(RuntimeError):
                module.performance.reasoning({**model, 'api_protocol': 'messages'}, 1024, metadata)

    def test_documented_alias_survives_tfl_hydration_and_pllm_consumption(self):
        for tfl_script, pllm_script in zip(TFL, PLLM):
            module = load_script(tfl_script)
            payload, metadata, prices = go_fixtures.GoMetadataTests().fixture(module)
            payload['data'][0].pop('reasoning_capabilities')
            metadata['models']['new-model']['reasoning'] = True
            proof = record(value={'supported_efforts': ['high', 'xhigh'],
                                  'effort_equivalence': 'thinking_enabled'})
            resolver = self.resolver(module, [proof])
            rows, excluded, findings = module.build_investigated(
                lambda data: module.build_rows(data, metadata, prices, blacklisted_models=()),
                payload, metadata, 'opencode_go', resolver)
            self.assertEqual(excluded, [])
            row = rows[0]
            raw = payload['data'][0]
            row['reasoning_capabilities'] = module.performance.capabilities(
                raw, module.go_model_metadata(raw, metadata), row)
            pllm = load_script(pllm_script)
            candidate = pllm.catalog_candidate(row, 'opencode_go', 1, DATE)
            self.assertEqual(candidate['model_investigations'], findings)
            self.assertEqual(pllm.performance.reasoning(candidate, 1024, candidate),
                             {'thinking': {'type': 'enabled'}})

    def test_pllm_rechecks_sources_before_any_generation(self):
        for script in PLLM:
            module = load_script(script)
            with patch.object(module.evidence_module, 'fetch_source', return_value=BODY):
                module.evidence_module.recheck_findings([record()], 'opencode_go', 'new-model', 'chat_completions')
            with patch.object(module.evidence_module, 'fetch_source', return_value=b'changed'):
                with self.assertRaisesRegex(RuntimeError, 'investigation'):
                    module.evidence_module.recheck_findings([record()], 'opencode_go', 'new-model', 'chat_completions')
            with self.assertRaisesRegex(RuntimeError, 'incompatible'):
                module.evidence_module.recheck_findings([record()], 'openrouter', 'new-model', 'chat_completions')

    def test_pllm_unknown_context_is_a_safe_exclusion_in_each_catalog(self):
        for script in PLLM:
            module = load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                for context in (None, True, '1000000', 999_999):
                    with self.assertRaisesRegex(RuntimeError, 'Contexte TFL'):
                        module.catalog_candidate({'id': 'new-model', 'context_length': context}, section, 1, DATE)

    def test_invalid_or_ambiguous_registry_stays_blocking(self):
        module = load_script(TFL[0])
        invalid = [record(value={'supported_efforts': ['medium']}),
                   record(value={'supported_efforts': None}), record(sources=[]),
                   record(value={'supported_efforts': ['high'], 'effort_equivalence': 'invented'})]
        unsafe = record()
        unsafe['sources'][0]['url'] = 'https://user:private@official.example/docs'
        invalid.append(unsafe)
        for value in invalid:
            with self.assertRaises(RuntimeError):
                self.resolver(module, [value])
        with self.assertRaisesRegex(RuntimeError, 'dupliquée'):
            self.resolver(module, [record(), record()])


if __name__ == '__main__':
    unittest.main()
