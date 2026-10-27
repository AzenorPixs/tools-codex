"""Contrats réels de requête et erreurs simulées, sans réseau ni secret réel."""

from datetime import datetime, timezone
from email.message import Message
from http.client import IncompleteRead
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from test_extension_qualification import load_script, PLLM
import test_pllm_free_fallback as free_tests


REFERENCE = datetime(2026, 10, 25, 9, 0, tzinfo=timezone.utc)


def failure(code, payload=None, retry=None, raw=None):
    headers = Message()
    if retry is not None:
        headers['Retry-After'] = retry
    body = raw if raw is not None else json.dumps(payload or {}).encode()
    return HTTPError('https://example.invalid/private', code, 'private reason', headers, io.BytesIO(body))


class PllmHttpDiagnosticsTests(unittest.TestCase):
    def modules(self):
        for script in PLLM:
            yield load_script(script)

    def test_chat_open_code_body_keeps_medium_without_thinking(self):
        for module in self.modules():
            for provider in ('opencodego', 'opencode'):
                model = {'model_id': 'unseen-fixture', 'provider': provider, 'api_protocol': 'chat_completions',
                         'api_endpoint': 'https://opencode.ai/inference/openai/v1/chat/completions'}
                stream = io.BytesIO(b'data: [DONE]\n')
                with patch.object(module, 'request', return_value=stream) as request:
                    with self.assertRaisesRegex(RuntimeError, 'Réponse absente'):
                        module.benchmark(model, 'offline-key', 1024, {'reasoning': {'supported_efforts': ['medium']}}, session_id='private-session')
                body = request.call_args.args[2]
                self.assertEqual(body['reasoning_effort'], 'medium')
                self.assertNotIn('thinking', body)
                self.assertEqual(body['max_tokens'], 1024)
                self.assertEqual(request.call_args.kwargs['extra_headers']['x-opencode-session'], 'private-session')
                self.assertNotIn('private-session', json.dumps(model))

    def test_other_reasoning_contracts_are_preserved(self):
        for module in self.modules():
            self.assertEqual(module.reasoning({'provider': 'deepseek'}, 1024, {'reasoning': {'supported_efforts': ['medium']}}),
                             {'reasoning_effort': 'medium', 'thinking': {'type': 'enabled'}})
            for provider in ('opencodego', 'opencode'):
                self.assertEqual(module.reasoning({'provider': provider, 'api_protocol': 'responses'}, 1024, {'reasoning': {'supported_efforts': ['medium']}}),
                                 {'reasoning': {'effort': 'medium'}})
                self.assertEqual(module.reasoning({'provider': provider, 'api_protocol': 'messages'}, 1024, {'reasoning': {'supported_efforts': ['medium']}}),
                                 {'thinking': {'type': 'adaptive'}, 'output_config': {'effort': 'medium'}})
            with self.assertRaisesRegex(RuntimeError, 'Medium'):
                module.reasoning({'provider': 'openrouter'}, 2048,
                                 {'reasoning': {'supports_max_tokens': True}})

    def test_retry_after_seconds_zero_and_whitespace(self):
        for module in self.modules():
            for value, seconds in (('120', 120), ('0', 0), (' 30 ', 30)):
                result = module.retry_after(value, REFERENCE)
                self.assertEqual(result['retry_after_seconds'], seconds)
                target = datetime.fromisoformat(result['retry_at'])
                self.assertEqual((target - REFERENCE).total_seconds(), seconds)
                self.assertIsNotNone(target.tzinfo)

    def test_retry_after_http_date_and_past_date(self):
        for module in self.modules():
            for value, seconds in (('Sun, 25 Oct 2026 09:02:00 GMT', 120),
                                   ('Sun, 25 Oct 2026 08:00:00 GMT', 0)):
                result = module.retry_after(value, REFERENCE)
                self.assertEqual(result['retry_after_seconds'], seconds)
                self.assertGreaterEqual(datetime.fromisoformat(result['retry_at']), REFERENCE)

    def test_retry_after_absent_negative_invalid_or_overflow_is_not_invented(self):
        for module in self.modules():
            for value in (None, '', ' ', '-1', '1.5', 'tomorrow', 'Sun, 25 Oct 2026 10:00:00',
                          '9' * 128, '9' * 129, 'Fri, 31 Dec 9999 23:59:59 GMT'):
                self.assertEqual(module.retry_after(value, REFERENCE),
                                 {'retry_after_seconds': None, 'retry_at': None})

    def test_unsupported_thinking_diagnostic_filters_private_message(self):
        for module in self.modules():
            error = failure(400, {'error': {'type': 'invalid_request_error', 'param': 'thinking',
                                          'message': 'Unsupported thinking parameter; private-key personal@example.invalid'}})
            diagnostic = module.http_diagnostic(error)
            self.assertEqual(diagnostic['parameter'], 'thinking')
            self.assertEqual(diagnostic['error_code'], 'invalid_request_error')
            self.assertIn('paramètre non pris en charge : thinking', module.error_message(error))
            self.assertNotIn('private-key', json.dumps(diagnostic))
            self.assertNotIn('personal@', json.dumps(diagnostic))
            self.assertNotIn('private reason', module.error_message(error))

    def test_parameter_is_inferred_only_from_known_names_and_rejection(self):
        for module in self.modules():
            for payload, expected in (({'error': {'message': 'Unrecognized request argument supplied: thinking'}}, 'thinking'),
                                      ({'error': {'message': 'Request mentions thinking'}}, None),
                                      ({'error': {'param': 'private-key', 'type': 'private-key'}}, None)):
                diagnostic = module.filtered_error(payload)
                self.assertEqual(diagnostic['parameter'], expected)
                self.assertNotIn('private-key', json.dumps(diagnostic))

    def test_invalid_value_and_missing_session_are_explicit(self):
        for module in self.modules():
            error = failure(400, {'error': {'code': 'invalid_value', 'param': 'max_tokens'}})
            self.assertIn('paramètre invalide : max_tokens', module.error_message(error))
            error = failure(400, {'error': {'name': 'MissingSessionID', 'message': 'private-session'}})
            self.assertEqual(module.error_message(error), 'HTTP 400 — session OpenCode manquante')
            self.assertNotIn('private-session', json.dumps(module.http_diagnostic(error)))

    def test_free_usage_limit_and_retry_at_are_visible(self):
        for module in self.modules():
            error = failure(429, {'error': 'Free usage limit exceeded for this model; personal@example.invalid'}, retry='120')
            with patch.object(module, 'retry_after', return_value={
                    'retry_after_seconds': 120, 'retry_at': '2026-10-25T09:02:00+00:00'}):
                text = module.error_message(error)
            self.assertIn('limite d’usage gratuit du modèle', text)
            self.assertIn('25-10-26 10:02 (Paris)', text)
            self.assertNotIn('personal@', text)
            self.assertEqual(module.http_diagnostic(error)['retry_after_seconds'], 120)

    def test_429_without_valid_retry_after_has_no_date(self):
        for module in self.modules():
            for header in (None, 'invalid', '-2'):
                error = failure(429, retry=header)
                self.assertEqual(module.error_message(error), 'HTTP 429 — limitation fournisseur')
                self.assertIsNone(module.http_diagnostic(error)['retry_at'])

    def test_non_json_empty_or_closed_body_keeps_status_and_closes(self):
        for module in self.modules():
            for raw in (b'', b'<html>private-key</html>', b'\xff'):
                error = failure(400, raw=raw)
                body = error.fp
                self.assertEqual(module.error_message(error), 'HTTP 400')
                self.assertTrue(body.closed)
                self.assertNotIn('private-key', json.dumps(module.http_diagnostic(error)))
            error = failure(400)
            error.close()
            self.assertEqual(module.error_message(error), 'HTTP 400')

    def test_body_read_is_bounded_and_diagnostic_cached(self):
        for module in self.modules():
            error = failure(400, raw=b'x' * 70000)
            body = error.fp
            with patch.object(body, 'read', wraps=body.read) as read:
                first = module.http_diagnostic(error)
                second = module.http_diagnostic(error)
                self.assertIs(first, second)
                read.assert_called_once_with(65536)
            self.assertEqual(first['body_status'], 'too_large')
            self.assertTrue(body.closed)
            self.assertNotIn('x' * 100, json.dumps(first))

    def test_unknown_private_error_does_not_become_a_code(self):
        for module in self.modules():
            error = failure(429, {'error': {'code': 'private-key', 'param': 'private-key',
                                          'message': 'private-key personal@example.invalid'}})
            diagnostic = module.http_diagnostic(error)
            self.assertIsNone(diagnostic['error_code'])
            self.assertIsNone(diagnostic['parameter'])
            self.assertNotIn('private-key', json.dumps(diagnostic))

    def test_incomplete_error_body_is_closed_without_losing_status(self):
        for module in self.modules():
            error = failure(429)
            body = error.fp
            with patch.object(body, 'read', side_effect=IncompleteRead(b'private-key')):
                self.assertEqual(module.error_message(error), 'HTTP 429 — limitation fournisseur')
            self.assertTrue(body.closed)
            self.assertNotIn('private-key', json.dumps(module.http_diagnostic(error)))

    def test_unknown_open_code_protocol_is_not_given_deepseek_parameters(self):
        for module in self.modules():
            self.assertEqual(module.reasoning({'provider': 'opencodego'}, 1024, {'reasoning': {'supported_efforts': ['medium']}}), {'reasoning_effort': 'medium'})
            with self.assertRaisesRegex(RuntimeError, 'Protocole API OpenCode'):
                module.reasoning({'provider': 'opencode', 'api_protocol': 'unknown'}, 1024, {'reasoning': {'supported_efforts': ['medium']}})

    def test_http_authentication_and_access_diagnostics_are_preserved(self):
        for module in self.modules():
            for code, text in ((401, 'Authentification refusée (HTTP 401)'), (403, 'Accès refusé (HTTP 403)')):
                error = failure(code, {'error': 'private-key'})
                self.assertEqual(module.error_message(error), text)
                self.assertEqual(module.is_authentication_error(error), code == 401)

    def test_sse_400_and_429_are_structured_and_filtered(self):
        for module in self.modules():
            for code, expected in ((400, 400), ('invalid_request_error', 400),
                                   (429, 429), ('rate_limit_error', 429)):
                error = module.api_error(code, {'code': 'unsupported_parameter', 'param': 'thinking',
                                               'message': 'Unsupported thinking; private-key'})
                self.assertIsInstance(error, module.ApiFailure)
                self.assertEqual(module.http_diagnostic(error)['http_status'], expected)
                self.assertNotIn('private-key', module.error_message(error))

    def test_normal_http_errors_do_not_invent_unsupported_parameters(self):
        for module in self.modules():
            error = failure(500, {'error': 'private error'})
            self.assertEqual(module.error_message(error), 'HTTP 500')

    def test_candidate_stops_on_400_429_and_continues_other_candidate(self):
        helper = free_tests.PllmFreeFallbackTests()
        self.addCleanup(helper.doCleanups)
        for script in PLLM:
            for code in (400, 429):
                module, path, _ = helper.workspace(script)

                def benchmark(model, budget):
                    if model['model_id'] == 'paid-a':
                        raise failure(code, {'error': {'type': 'unsupported_parameter', 'param': 'thinking'}}, retry='120')
                    model.update(ttft_seconds=5, tokens_per_second=40)
                    return True

                data, events, _ = helper.run_evaluation(module, path, benchmark_behavior=benchmark, active=True)
                calls = [event for event in events if event[0] == 'benchmark']
                self.assertEqual([event[2] for event in calls], ['paid-a', 'paid-b'])
                self.assertEqual(data['models'][0]['model_id'], 'paid-b')
                failed = data['models'][0]['candidate_results'][0]
                self.assertEqual(len(failed['performance_test']['attempts']), 1)
                self.assertEqual(failed['performance_test']['attempts'][0]['http_error']['http_status'], code)

    def test_sse_rate_limit_does_not_increase_budget(self):
        helper = free_tests.PllmFreeFallbackTests()
        self.addCleanup(helper.doCleanups)
        for script in PLLM:
            module, path, _ = helper.workspace(script)

            def benchmark(model, budget):
                raise module.api_error('rate_limit_exceeded', {'message': 'private-key'})

            data, events, _ = helper.run_evaluation(module, path, benchmark_behavior=benchmark,
                                                  forced={'mode': 'mode1', 'rank': 2})
            self.assertEqual(len([event for event in events if event[0] == 'benchmark']), 1)
            self.assertEqual(data['models'][0]['state'], 'Invalide')

    def test_truncation_still_advances_budget_and_only_success_is_remembered(self):
        helper = free_tests.PllmFreeFallbackTests()
        self.addCleanup(helper.doCleanups)
        for script in PLLM:
            module, path, _ = helper.workspace(script)

            def benchmark(model, budget):
                model.update(ttft_seconds=5, tokens_per_second=40)
                return budget == 2048

            data, events, _ = helper.run_evaluation(module, path, benchmark_behavior=benchmark,
                                                  forced={'mode': 'mode1', 'rank': 2})
            self.assertEqual([event[3] for event in events if event[0] == 'benchmark'], [1024, 2048])
            self.assertEqual(data['models'][0]['last_successful_max_tokens'], 2048)
            self.assertEqual(module.load_memory()['policies']['mode1']['last_successful_max_tokens'], 2048)

    def test_failed_candidate_publishes_details_without_private_content(self):
        helper = free_tests.PllmFreeFallbackTests()
        self.addCleanup(helper.doCleanups)
        for script in PLLM:
            for code in (400, 429):
                module, path, _ = helper.workspace(script)

                def benchmark(model, budget):
                    if code == 400:
                        payload = {'error': {'type': 'unsupported_parameter', 'param': 'thinking',
                                             'message': 'Unsupported thinking; private-key personal@example.invalid'}}
                    else:
                        payload = {'error': 'Free usage limit exceeded for this model; private-key personal@example.invalid'}
                    raise failure(code, payload, retry='120')

                data, events, output = helper.run_evaluation(module, path, benchmark_behavior=benchmark,
                                                            forced={'mode': 'mode1', 'rank': 2})
                model = data['models'][0]
                self.assertEqual(model['state'], 'Invalide')
                self.assertEqual(model['performance_test']['http_error']['http_status'], code)
                self.assertEqual(len([event for event in events if event[0] == 'benchmark']), 1)
                self.assertNotIn('private-key', json.dumps(data))
                self.assertNotIn('personal@', json.dumps(data))
                self.assertIn('thinking' if code == 400 else 'réessai à partir du', output)


if __name__ == '__main__':
    unittest.main()
