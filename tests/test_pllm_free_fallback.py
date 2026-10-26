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
        installed.with_name('performance.py').write_bytes(script.with_name('performance.py').read_bytes())
        installed.with_name('model_blacklist.py').write_bytes(script.with_name('model_blacklist.py').read_bytes())
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
                       benchmark_behavior=None, secret_ok=True, secret_lookup=None, **kwargs):
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
            if model['mode'] in module.FREE_MODES:
                self.assertFalse(any(event[0] == 'quota' and event[1] == model['mode'] for event in events))
            else:
                self.assertEqual(events[-2][0], 'quota')
            model['performance_test'] = {'status': 'running', 'max_tokens': budget, 'requests': 1}
            complete = True
            if benchmark_behavior:
                complete = benchmark_behavior(model, budget)
            else:
                model.update(ttft_seconds=5, tokens_per_second=40 if model['model_id'] in ('paid-b', 'free-general') else 25)
            model['performance_test']['status'] = 'completed' if complete else 'truncated'
            return complete

        metadata = [{'id': item['id'], 'reasoning': {'supported_efforts': ['high']}}
                    for item in json.loads(path.read_text())['openrouter']['models']]
        with ExitStack() as stack:
            stack.enter_context(patch.object(module.subprocess, 'run', side_effect=secret_lookup, return_value=SimpleNamespace(
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

    def test_available_resources_only_benchmark_first_valid_paid(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, events, output = self.run_evaluation(module, path, active=True)
            self.assertEqual(data['selected_mode'], 'mode1')
            self.assertEqual(data['models'][0]['model_id'], 'paid-a')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['paid-a'])
            self.assertFalse(any(event[1] != 'mode1' for event in events))
            self.assertEqual(output, '')

    def test_paid_go_modes_exhausted_and_free_modes_independent(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            data, events, output = self.run_evaluation(module, path, exhausted=True)
            for model in data['models'][:2]:
                self.assertEqual(model['state'], 'Invalide')
                self.assertEqual(model['quota_status'], 'exhausted')
                self.assertEqual(model['quotas']['weekly']['percent'], 100)
                self.assertIn('Hebdo : 0 %', model['quota_display']['text'])
                self.assertFalse(any(event[0] == 'benchmark' and event[1] == model['mode'] for event in events))
            for model in data['models'][2:4]:
                self.assertEqual((model['model_id'], model['provider'], model['state']),
                                 ('free-go', 'opencodego', 'Valide'))
                self.assertIsNone(model['quotas'])
                self.assertEqual(model['quota_status'], 'not_applicable')
                self.assertEqual(model['selection_category'], 'free')
                self.assertIn('Non applicable', model['quota_display']['text'])
            self.assertEqual(data['selected_mode'], 'mode3')
            self.assertIn('🟢 Valide — gratuit', output)
            self.assertIn('🔴 Invalide — Quota épuisé', output)

    def test_openrouter_exhausted_never_generates_and_next_run_can_recover(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            first, events, _ = self.run_evaluation(module, path, exhausted=True, forced={'mode': 'mode5'})
            self.assertEqual(first['models'][4]['state'], 'Invalide')
            self.assertEqual(first['models'][4]['quota_status'], 'exhausted')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], [])
            second, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode5'})
            self.assertEqual(second['models'][4]['model_id'], 'paid-router')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['paid-router'])

    def test_free_winner_history_keeps_its_category_when_go_recovers(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            def first_run(model, budget):
                model.update(ttft_seconds=30 if model['model_id'] == 'free-go' else 5,
                             tokens_per_second=40)
                return True

            self.run_evaluation(module, path, exhausted=True, benchmark_behavior=first_run, active=True)
            self.assertEqual(module.load_current()['models'][2]['provider'], 'opencode')
            data, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode3'})
            self.assertEqual(data['models'][2]['model_id'], 'free-go')
            self.assertTrue(all(event[0] != 'quota' for event in events))
            self.assertTrue(all(event[2].startswith('free-') for event in events))

    def test_catalog_order_breaks_free_price_ties_without_comparison(self):
        for script in PLLM:
            for equal_ttft in (False, True):
                module, path, _ = self.workspace(script)

                def behavior(model, budget):
                    model.update(ttft_seconds=5 if equal_ttft or model['model_id'] == 'paid-b' else 10,
                                 tokens_per_second=40)
                    return True

                data, _, _ = self.run_evaluation(module, path, benchmark_behavior=behavior, active=True)
                self.assertEqual(data['models'][0]['model_id'], 'paid-a')

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

            data, events, _ = self.run_evaluation(module, path, quota_behavior=unavailable, forced={'mode': 'mode1'})
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
                relevant = [event for event in events if event[0] == 'benchmark' and event[1] == 'mode3']
                self.assertEqual(len(relevant), 0 if empty else 8)
                self.assertTrue(all(event[2].startswith('free-') for event in relevant))

    def test_success_does_not_contact_next_candidate_with_unusable_authentication(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def behavior(model, budget):
                if model['model_id'] == 'paid-b':
                    raise http_error(401)
                model.update(ttft_seconds=5, tokens_per_second=25)
                return True

            data, events, output = self.run_evaluation(module, path, benchmark_behavior=behavior)
            self.assertEqual(data['models'][0]['state'], 'Valide')
            self.assertEqual(data['models'][0]['ttft_seconds'], 5)
            self.assertNotIn('Authentification refusée (HTTP 401)', output)
            self.assertEqual(len([event for event in events if event[0] == 'benchmark' and event[1] == 'mode1']), 1)

    def test_authentication_failure_on_next_candidate_after_failure_invalidates_mode(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def behavior(model, budget):
                if model['model_id'] == 'paid-b':
                    raise http_error(401)
                model.update(ttft_seconds=5, tokens_per_second=10)
                return True

            data, events, output = self.run_evaluation(module, path, benchmark_behavior=behavior, active=True)
            self.assertEqual(data['models'][0]['state'], 'Invalide')
            self.assertIn('Authentification refusée (HTTP 401)', data['models'][0]['cause'])
            self.assertEqual(output, '')
            self.assertEqual([e[2] for e in events if e[0] == 'benchmark' and e[1] == 'mode1'],
                             ['paid-a'] * 4 + ['paid-b'])

    def test_paid_go_recovers_only_on_next_evaluation(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)
            first, events, _ = self.run_evaluation(module, path, exhausted=True, forced={'mode': 'mode1'})
            self.assertEqual(first['models'][0]['state'], 'Invalide')
            self.assertFalse(any(event[0] == 'benchmark' for event in events))
            second, events, _ = self.run_evaluation(module, path, forced={'mode': 'mode1'})
            self.assertEqual(second['models'][0]['model_id'], 'paid-a')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark'], ['paid-a'])

    def test_openrouter_oscillating_resources_are_bounded(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def oscillating(model, events):
                return len([event for event in events if event[0] == 'quota']) % 2 == 1

            def fail(model, budget):
                model.update(ttft_seconds=90, tokens_per_second=15)
                return True

            data, events, _ = self.run_evaluation(module, path, quota_behavior=oscillating,
                                                  benchmark_behavior=fail)
            router = data['models'][4]
            self.assertEqual(router['state'], 'Invalide')
            router_calls = [event for event in events if event[1] == 'mode5']
            self.assertLessEqual(len(router_calls), 4)

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
            def behavior(model, budget):
                model.update(ttft_seconds=30 if model['provider'] == 'opencodego' else 5,
                             tokens_per_second=40)
                return True

            data, events, _ = self.run_evaluation(module, path, exhausted=True,
                                                  benchmark_behavior=behavior, active=True)
            calls = [event for event in events if event[0] == 'benchmark']
            self.assertEqual([event[-1] for event in calls], ['opencodego'] * 4 + ['opencode'])
            self.assertEqual(data['models'][2]['provider'], 'opencode')

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
            self.assertEqual(len(memory['configurations']), 1)
            selected = first['models'][0]
            self.assertEqual(module.budgets_for(selected, module.load_memory())[0], 1024)

            def next_candidate(model, budget):
                model.update(ttft_seconds=5, tokens_per_second=10 if model['model_id'] == 'paid-a' else 40)
                return True

            second, _, _ = self.run_evaluation(module, path, benchmark_behavior=next_candidate, active=True)
            self.assertEqual(second['models'][0]['model_id'], 'paid-b')
            self.assertEqual(len(module.load_memory()['policies']['mode1']['configurations']), 2)
            self.assertEqual(second['models'][0]['performance_test']['attempts'][0]['max_tokens'], 1024)
            third, _, _ = self.run_evaluation(module, path, secret_ok=False, active=True)
            self.assertIsNone(third['models'][0]['last_successful_max_tokens'])

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
                self.assertEqual(model['tokens_per_second'], 20.2)
                self.assertEqual(model['throughput_scope'], 'reasoning_and_response')
                self.assertEqual(request.call_args.args[2]['reasoning'], {'effort': 'high'})
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
            model = {'mode': 'mode5', 'provider': 'openrouter', 'model_id': 'fixture'}
            with patch.object(module, 'request', return_value=stream) as request, \
                    patch.object(module.time, 'monotonic', side_effect=(0, 1, 2, 3, 4, 5)):
                self.assertTrue(module.benchmark(model, 'offline-fixture', 1024,
                                                {'reasoning': {'supported_efforts': ['high']}}))
            self.assertEqual(model['tokens_per_second'], 4.2)
            self.assertEqual(model['throughput_scope'], 'response_only')
            self.assertEqual(request.call_args.args[2]['reasoning'], {'effort': 'high'})
            self.assertNotIn('provider', request.call_args.args[2])

    def test_success_does_not_check_quota_for_next_candidate(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def unavailable(model, events):
                if model['model_id'] == 'paid-b':
                    raise RuntimeError('Quota indispensable indisponible')
                return False

            data, events, _ = self.run_evaluation(module, path, quota_behavior=unavailable, active=True)
            self.assertEqual(data['models'][0]['state'], 'Valide')
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark' and event[1] == 'mode1'], ['paid-a'])
            self.assertFalse(any(event[0] == 'quota' and event[2] == 'paid-b' for event in events))

    def test_quota_failure_before_next_candidate_after_failure_blocks_generation(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def unavailable(model, events):
                if model['model_id'] == 'paid-b':
                    raise RuntimeError('Quota indispensable indisponible')
                return False

            def fail(model, budget):
                model.update(ttft_seconds=5, tokens_per_second=10)
                return True

            data, events, _ = self.run_evaluation(module, path, quota_behavior=unavailable,
                                                  benchmark_behavior=fail, active=True)
            self.assertEqual(data['models'][0]['state'], 'Invalide')
            self.assertEqual([e[2] for e in events if e[0] == 'benchmark' and e[1] == 'mode1'], ['paid-a'] * 4)

    def test_paid_quota_exhaustion_between_failed_tiers_stops_without_free_fallback(self):
        for script in PLLM:
            module, path, _ = self.workspace(script)

            def exhausted_after_first(model, events):
                return any(event[0] == 'benchmark' for event in events)

            def fail(model, budget):
                model.update(ttft_seconds=5, tokens_per_second=10 if model['mode'] == 'mode1' else 40)
                return True

            data, events, _ = self.run_evaluation(module, path, quota_behavior=exhausted_after_first,
                                                  benchmark_behavior=fail, active=True)
            self.assertEqual(data['models'][0]['state'], 'Invalide')
            self.assertEqual(data['models'][0]['selection_category'], 'paid')
            self.assertIsNone(data['models'][0]['ttft_seconds'])
            self.assertEqual([event[2] for event in events if event[0] == 'benchmark' and event[1] == 'mode1'], ['paid-a'])
            self.assertEqual(data['selected_mode'], 'mode3')

    def test_high_incompatible_metadata_prevents_generation(self):
        for script in PLLM:
            module, _, _ = self.workspace(script)
            model = {'mode': 'mode5', 'provider': 'openrouter', 'model_id': 'fixture'}
            with patch.object(module, 'request') as request, self.assertRaisesRegex(RuntimeError, 'HIGH et XHIGH non pris en charge'):
                module.benchmark(model, 'offline-fixture', 1024, {'reasoning': {'supported_efforts': ['low']}})
            request.assert_not_called()


if __name__ == '__main__':
    unittest.main()
