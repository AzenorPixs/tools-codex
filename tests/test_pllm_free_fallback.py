"""Sélection PLLM et diagnostics observables, sans réseau ni trousseau réel."""

from contextlib import ExitStack
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from test_extension_qualification import load_script, ROOT, PLLM


def row(name, section='opencode_go', free=False):
    price = 0 if free else 0.1
    result = {'id': name, 'context_length': 1_000_000, 'output_modalities': ['text']}
    if section == 'openrouter':
        result.update(input_price=price, output_price=price)
    else:
        keys = ('input_off_peak', 'output_off_peak') if section == 'opencode_go' else ('input', 'output')
        result.update(available=True, api_protocol='responses',
                      api_endpoint='https://opencode.ai/zen/' + ('go/' if section == 'opencode_go' else '') + 'v1/responses',
                      reference_pricing_usd_per_million_tokens=dict.fromkeys(keys, price))
    return result


def http_error(code):
    error = HTTPError('https://example.invalid', code, 'fixture privée', {}, io.BytesIO())
    error.close()
    return error


class PllmFreeFallbackTests(unittest.TestCase):
    def workspace(self, script):
        temporary = tempfile.TemporaryDirectory(prefix='pllm-free-', dir=ROOT / 'tests')
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        installed = base / 'pllm/scripts/evaluate.py'
        installed.parent.mkdir(parents=True)
        installed.write_bytes(script.read_bytes())
        module = load_script(installed)
        path = base / 'catalog.json'
        catalog = {'generated_at': 'fixture-date',
                   'opencode_go': {'models': [row('free-go', free=True), row('paid-a'), row('paid-b')]},
                   'opencode': {'models': [row('free-general', 'opencode', True)]},
                   'openrouter': {'models': [row('free-router', 'openrouter', True),
                                             row('paid-router', 'openrouter')]}}
        path.write_text(json.dumps(catalog))
        return module, path, catalog

    def run_evaluation(self, module, path, exhausted=False, quota_behavior=None,
                       benchmark_behavior=None, secret_ok=True, **kwargs):
        events = []

        def quota(model, key):
            events.append(('quota', model['mode'], model['model_id']))
            depleted = exhausted
            if quota_behavior:
                depleted = quota_behavior(model, events)
            if model['mode'] in ('mode1', 'mode2'):
                model['quota_provider'] = 'opencodego'
                model['quotas'] = {period: {'percent': 100 if depleted else 10,
                                          'status': 'rate-limited' if depleted else 'ok'}
                                   for period in ('rolling', 'weekly', 'monthly')}
            else:
                model['quotas'] = {'balance': 0 if depleted else 10, 'currency': 'USD'}
            if depleted:
                raise module.QuotaExhausted('Quota épuisé')

        def benchmark(model, key, budget, metadata, session_id=None):
            events.append(('benchmark', model['mode'], model['model_id'], budget, model['provider']))
            self.assertEqual(events[-2][0], 'quota')
            model['performance_test'] = {'status': 'running', 'max_tokens': budget, 'requests': 1}
            complete = True
            if benchmark_behavior:
                complete = benchmark_behavior(model, budget)
            else:
                model.update(ttft_seconds=5, tokens_per_second=40 if model['model_id'] in ('paid-b', 'free-general') else 25)
            model['performance_test']['status'] = 'completed' if complete else 'truncated'
            return complete

        metadata = [{'id': item['id'], 'reasoning': {'supported_efforts': ['low']}}
                    for item in json.loads(path.read_text())['openrouter']['models']]
        with ExitStack() as stack:
            stack.enter_context(patch.object(module.subprocess, 'run', return_value=SimpleNamespace(
                returncode=0 if secret_ok else 1, stdout=b'offline-fixture' if secret_ok else b'')))
            stack.enter_context(patch.object(module, 'quota', side_effect=quota))
            stack.enter_context(patch.object(module, 'benchmark', side_effect=benchmark))
            stack.enter_context(patch.object(module, 'get', return_value={'data': metadata}))
            stack.enter_context(patch.object(module, 'exchange_rates', return_value={'rates': {'USD': 1}}))
            stack.enter_context(patch.object(module.urllib.request, 'urlopen', side_effect=AssertionError('Réseau interdit')))
            output = stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))
            module.main(tfl_catalog=path, **kwargs)
        data = json.loads((module.ROOT / 'data/pllm-current.json').read_text())
        return data, events, output.getvalue()

    def test_available_resources_only_benchmark_paid_and_choose_fastest(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, events, output = self.run_evaluation(module, path, active=True)
            self.assertEqual(data['selected_mode'], 'mode1')
            self.assertEqual(data['models'][0]['model_id'], 'paid-b')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['paid-a', 'paid-b'])
            self.assertFalse(any(event[1] != 'mode1' for event in events))
            self.assertEqual(output, '')

    def test_both_go_modes_include_general_free_and_keep_exhausted_quotas(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, events, output = self.run_evaluation(module, path, exhausted=True)
            for model in data['models'][:2]:
                self.assertEqual((model['model_id'], model['provider'], model['state']),
                                 ('free-general', 'opencode', 'Valide'))
                self.assertEqual(model['quotas']['weekly']['percent'], 100)
                self.assertEqual(model['selection_category'], 'free')
                self.assertIn('Hebdo : 0 %', model['quota_display']['text'])
            self.assertIn('🟢 Valide — repli gratuit', output)
            self.assertTrue(all(event[2].startswith('free-') for event in events
                                if event[0] == 'benchmark' and event[1] != 'mode4'))

    def test_openrouter_free_only_when_credit_exhausted_and_returns_to_paid(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            first, events, _ = self.run_evaluation(module, path, exhausted=True, forced={'mode': 'mode3'})
            self.assertEqual(first['models'][2]['model_id'], 'free-router')
            self.assertEqual(first['models'][2]['state'], 'Valide')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['free-router'])
            second, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode3'})
            self.assertEqual(second['models'][2]['model_id'], 'paid-router')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['paid-router'])

    def test_general_winner_history_reloads_with_original_go_account(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            self.run_evaluation(module, path, exhausted=True, active=True)
            self.assertEqual(module.load_current()['models'][0]['provider'], 'opencode')
            data, events, _ = self.run_evaluation(module, path, active=True)
            self.assertEqual(data['models'][0]['provider'], 'opencodego')
            self.assertEqual(data['models'][0]['model_id'], 'paid-b')
            self.assertFalse(any(event[2].startswith('free-') for event in events if event[0] == 'benchmark'))

    def test_ttft_then_catalog_order_break_ties(self):
        for script in PLLM:
            for equal_ttft, expected in ((False, 'paid-b'), (True, 'paid-a')):
                module, path, _ = self.workspace(script)

                def behavior(model, budget):
                    model.update(ttft_seconds=5 if equal_ttft or model['model_id'] == 'paid-b' else 10,
                                 tokens_per_second=40)
                    return True

                data, _, _ = self.run_evaluation(module, path, benchmark_behavior=behavior, active=True)
                self.assertEqual(data['models'][0]['model_id'], expected)

    def test_lower_priority_faster_mode_does_not_replace_first_valid(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def behavior(model, budget):
                model.update(ttft_seconds=5, tokens_per_second=20 if model['mode'] == 'mode1' else 100)
                return True

            data, _, _ = self.run_evaluation(module, path, benchmark_behavior=behavior)
            self.assertEqual(data['selected_mode'], 'mode1')

    def test_http_authentication_errors_visible_without_free_fallback(self):
        for script in PLLM:
            for code, diagnostic in ((401, 'Authentification refusée (HTTP 401)'), (403, 'Accès refusé (HTTP 403)')):
                module, path, _ = self.workspace(script)

                def quota_error(model, events):
                    raise http_error(code)

                data, events, output = self.run_evaluation(module, path, quota_behavior=quota_error,
                                                          forced={'mode': 'mode2'})
                self.assertEqual(data['models'][1]['state'], 'Invalide')
                self.assertIn(diagnostic, output)
                self.assertFalse(any(event[0] == 'benchmark' for event in events))
                self.assertNotIn('fixture privée', output)

    def test_missing_secret_visible_and_no_benchmark(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, events, output = self.run_evaluation(module, path, secret_ok=False)
            self.assertEqual(events, [])
            self.assertIn('Clé API inaccessible', output)
            self.assertIsNone(data['selected_mode'])

    def test_quota_unavailable_is_not_exhaustion(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def unavailable(model, events):
                raise RuntimeError('Source de quota indisponible')

            data, events, _ = self.run_evaluation(module, path, quota_behavior=unavailable)
            self.assertFalse(any(event[0] == 'benchmark' for event in events))
            self.assertIsNone(data['selected_mode'])

    def test_no_free_candidate_or_only_free_performance_failures_stays_invalid(self):
        for script in PLLM:
            for empty in (True, False):
                module, path, catalog = self.workspace(script)
                if empty:
                    catalog['opencode_go']['models'] = [row('paid-a')]
                    catalog['opencode']['models'] = []
                    path.write_text(json.dumps(catalog))

                def fail(model, budget):
                    model.update(ttft_seconds=90, tokens_per_second=15)
                    return True

                data, events, _ = self.run_evaluation(module, path, exhausted=True,
                                                      benchmark_behavior=fail, active=True)
                self.assertIsNone(data['selected_mode'])
                relevant = [event for event in events if event[0] == 'benchmark' and event[1] == 'mode1']
                self.assertEqual(len(relevant), 0 if empty else 8)
                self.assertTrue(all(event[2].startswith('free-') for event in relevant))

    def test_authentication_failure_after_success_invalidates_mode(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def behavior(model, budget):
                if model['model_id'] == 'paid-b':
                    raise http_error(401)
                model.update(ttft_seconds=5, tokens_per_second=25)
                return True

            data, events, output = self.run_evaluation(module, path, benchmark_behavior=behavior)
            self.assertEqual(data['models'][0]['state'], 'Invalide')
            self.assertIsNone(data['models'][0]['ttft_seconds'])
            self.assertIn('Authentification refusée (HTTP 401)', output)
            self.assertEqual(len([event for event in events if event[0] == 'benchmark' and event[1] == 'mode1']), 2)

    def test_recovered_resources_switch_to_paid_before_free_generation(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def recovered(model, events):
                return len([event for event in events if event[0] == 'quota']) == 1

            data, events, _ = self.run_evaluation(module, path, quota_behavior=recovered, active=True)
            self.assertEqual(data['models'][0]['model_id'], 'paid-b')
            self.assertFalse(any(event[2].startswith('free-') for event in events if event[0] == 'benchmark'))

    def test_oscillating_resources_are_bounded(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def oscillating(model, events):
                return len([event for event in events if event[0] == 'quota']) % 2 == 1

            data, events, _ = self.run_evaluation(module, path, quota_behavior=oscillating, active=True)
            self.assertIsNone(data['selected_mode'])
            self.assertFalse(any(event[0] == 'benchmark' for event in events))
            self.assertLessEqual(len(events), 13)

    def test_forced_rank_cannot_substitute_free_or_paid(self):
        for script in PLLM:
            for exhausted, rank in ((True, 2), (False, 1)):
                module, path, _ = self.workspace(script)
                data, events, _ = self.run_evaluation(module, path, exhausted=exhausted,
                                                      forced={'mode': 'mode1', 'rank': rank})
                self.assertIsNone(data['selected_mode'])
                self.assertFalse(any(event[0] == 'benchmark' for event in events))

    def test_same_id_different_catalogs_are_separate_candidates(self):
        for script in PLLM:
            module, path, catalog = self.workspace(script)
            catalog['opencode']['models'][0]['id'] = 'free-go'
            path.write_text(json.dumps(catalog))
            data, events, _ = self.run_evaluation(module, path, exhausted=True, active=True)
            calls = [event for event in events if event[0] == 'benchmark']
            self.assertEqual([event[-1] for event in calls], ['opencodego', 'opencode'])
            self.assertEqual(data['models'][0]['provider'], 'opencodego')

    def test_eligibility_checks_prices_context_protocol_and_endpoint(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            for update in ({'context_length': 200_000}, {'api_endpoint': 'https://evil.invalid/responses'},
                           {'api_protocol': 'unknown'}, {'output_modalities': ['audio']},
                           {'reference_pricing_usd_per_million_tokens': {'input_off_peak': float('nan'), 'output_off_peak': 0}},
                           {'reference_pricing_usd_per_million_tokens': {'input_off_peak': -1, 'output_off_peak': 0}}):
                candidate = row('looks-free', free=True)
                candidate.update(update)
                with self.assertRaises((ValueError, RuntimeError)):
                    module.catalog_candidate(candidate, 'opencode_go', 1, 'fixture')
            paid = row('looks-free')
            self.assertFalse(module.catalog_candidate(paid, 'opencode_go', 1, 'fixture')['is_free'])
            variant = row('off-peak-free', free=True)
            variant['pricing_variants'] = [{'input': 0.1, 'output': 0.1}]
            self.assertFalse(module.catalog_candidate(variant, 'opencode_go', 1, 'fixture')['is_free'])

    def test_real_quota_parser_distinguishes_exhaustion_from_unknown_status(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            for status, percent, error in (('rate-limited', 100, module.QuotaExhausted),
                                           ('unknown', 100, RuntimeError), ('rate-limited', 50, RuntimeError)):
                quotas = {period: {'percent': percent, 'status': status} for period in ('rolling', 'weekly', 'monthly')}
                model = {'mode': 'mode1', 'provider': 'opencode'}
                with patch.object(module, 'get', return_value={'usage': quotas}), self.assertRaises(error) as raised:
                    module.quota(model, 'offline-fixture')
                if status == 'unknown' or percent == 50:
                    self.assertNotIsInstance(raised.exception, module.QuotaExhausted)

    def test_sse_authentication_diagnostic_does_not_expose_message(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            stream = io.BytesIO(b'data: {"error":{"code":401,"message":"private-message"}}\n')
            model = {'mode': 'mode1', 'model_id': 'fixture', 'provider': 'opencode',
                     'api_protocol': 'responses', 'api_endpoint': 'https://opencode.ai/zen/v1/responses'}
            with patch.object(module, 'request', return_value=stream), self.assertRaises(module.AuthenticationFailure) as error:
                module.benchmark(model, 'offline-fixture', 1024, {}, session_id='fixture')
            self.assertIn('HTTP 401', str(error.exception))
            self.assertNotIn('private-message', str(error.exception))

    def test_per_configuration_memory_and_no_stale_displayed_tier(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            first, _, _ = self.run_evaluation(module, path, active=True)
            memory = module.load_memory()['policies']['mode1']
            self.assertEqual(len(memory['configurations']), 2)
            selected = first['models'][0]
            self.assertEqual(module.budgets_for(selected, module.load_memory())[0], 1024)
            second, _, _ = self.run_evaluation(module, path, secret_ok=False, active=True)
            self.assertIsNone(second['models'][0]['last_successful_max_tokens'])

    def test_go_and_general_streams_use_same_global_throughput_and_low(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            for provider in ('opencodego', 'opencode'):
                events = [
                    {'type': 'response.reasoning_text.delta', 'delta': 'think'},
                    {'type': 'response.output_text.delta', 'delta': 'code'},
                    {'type': 'response.output_text.delta', 'delta': 'more'},
                    {'type': 'response.completed', 'response': {'status': 'completed', 'usage': {'output_tokens': 101}}},
                ]
                stream = io.BytesIO(b''.join(b'data: ' + json.dumps(event).encode() + b'\n' for event in events))
                model = {'mode': 'mode1', 'provider': provider, 'model_id': 'fixture',
                         'api_protocol': 'responses', 'api_endpoint': 'https://opencode.ai/zen/v1/responses'}
                with patch.object(module, 'request', return_value=stream) as request, \
                        patch.object(module.time, 'monotonic', side_effect=(0, 1, 2, 3, 4, 5)):
                    self.assertTrue(module.benchmark(model, 'offline-fixture', 1024, {}, session_id='stable-fixture'))
                self.assertEqual(model['ttft_seconds'], 2)
                self.assertEqual(model['tokens_per_second'], 50)
                self.assertEqual(model['throughput_scope'], 'reasoning_and_response')
                self.assertEqual(request.call_args.args[2]['reasoning'], {'effort': 'low'})
                self.assertEqual(request.call_args.kwargs['extra_headers']['x-opencode-session'], 'stable-fixture')
                self.assertNotIn('stable-fixture', json.dumps(model))

    def test_openrouter_response_only_throughput_and_low(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            events = [
                {'choices': [{'delta': {'reasoning': 'think'}}]},
                {'choices': [{'delta': {'content': 'code'}}]},
                {'choices': [{'delta': {'content': 'more'}, 'finish_reason': 'stop'}],
                 'usage': {'completion_tokens': 101, 'completion_tokens_details': {'reasoning_tokens': 80}}},
            ]
            stream = io.BytesIO(b''.join(b'data: ' + json.dumps(event).encode() + b'\n' for event in events) + b'data: [DONE]\n')
            model = {'mode': 'mode3', 'provider': 'openrouter', 'model_id': 'fixture'}
            with patch.object(module, 'request', return_value=stream) as request, \
                    patch.object(module.time, 'monotonic', side_effect=(0, 1, 2, 3, 4, 5)):
                self.assertTrue(module.benchmark(model, 'offline-fixture', 1024,
                                                {'reasoning': {'supported_efforts': ['low']}}))
            self.assertEqual(model['tokens_per_second'], 20)
            self.assertEqual(model['throughput_scope'], 'response_only')
            self.assertEqual(request.call_args.args[2]['reasoning'], {'effort': 'low'})
            self.assertNotIn('provider', request.call_args.args[2])

    def test_quota_failure_after_first_winner_invalidates_without_more_generation(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def unavailable(model, events):
                if model['model_id'] == 'paid-b':
                    raise RuntimeError('Quota indispensable indisponible')
                return False

            data, events, _ = self.run_evaluation(module, path, quota_behavior=unavailable, active=True)
            self.assertEqual(data['models'][0]['state'], 'Invalide')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark' and event[1] == 'mode1'], ['paid-a'])

    def test_paid_quota_exhaustion_discards_paid_winner_and_tests_only_free(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def exhausted_after_first(model, events):
                return any(event[0] == 'benchmark' for event in events)

            data, events, _ = self.run_evaluation(module, path, quota_behavior=exhausted_after_first, active=True)
            self.assertEqual(data['models'][0]['model_id'], 'free-general')
            self.assertEqual(data['models'][0]['selection_category'], 'free')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['paid-a', 'free-go', 'free-general'])

    def test_low_incompatible_metadata_prevents_generation(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            model = {'mode': 'mode3', 'provider': 'openrouter', 'model_id': 'fixture'}
            with patch.object(module, 'request') as request, self.assertRaisesRegex(RuntimeError, 'Low non pris en charge'):
                module.benchmark(model, 'offline-fixture', 1024, {'reasoning': {'supported_efforts': ['high']}})
            request.assert_not_called()


if __name__ == '__main__':
    unittest.main()
