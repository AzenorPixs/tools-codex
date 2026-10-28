"""Seuil EUR inclusif, provenance et échecs de conversion sans publication."""
import io
import unittest
from unittest.mock import patch

from eur_fixtures import FX
from test_extension_qualification import PLLM, TFL, load_script
from test_pllm_free_fallback import row


class OpenRouterEurTests(unittest.TestCase):
    def test_paid_and_free_without_medium_are_retained_for_their_distinct_policies(self):
        for script in TFL:
            module = load_script(script)
            payload = {'data': [
                {'id': 'paid-no-medium', 'name': 'Paid without Medium', 'context_length': 1_000_000,
                 'pricing': {'prompt': '0.0000001', 'completion': '0.0000002'},
                 'architecture': {'output_modalities': ['text']}},
                {'id': 'free-no-medium', 'name': 'Free without Medium', 'context_length': 1_000_000,
                 'pricing': {'prompt': '0', 'completion': '0'},
                 'architecture': {'output_modalities': ['text']}},
            ]}
            rows, excluded = module.build_openrouter_rows(payload, (), exchange_rates=FX)
            self.assertEqual([row['id'] for row in rows], ['free-no-medium', 'paid-no-medium'])
            self.assertEqual([row['reasoning'] for row in rows], ['medium', None])
            self.assertTrue(all(row['reasoning_capabilities'] == {} for row in rows))
            self.assertEqual(excluded, [])

    def test_non_unit_rate_and_exact_boundary_without_rounding(self):
        for script in (*TFL, *PLLM):
            engine = load_script(script).performance
            self.assertEqual(engine.openrouter_eur_prices('0.25', '0.25', FX)['average_eur'], .1)
            with self.assertRaisesRegex(RuntimeError, '0.10 €/M'):
                engine.openrouter_eur_prices('0.25', '0.25000000000000001', FX)
            below = engine.openrouter_eur_prices('0.1', '0.2', FX)
            self.assertEqual(below['average_eur'], .06)

    def test_unverifiable_rates_never_use_default_or_old_cost(self):
        for script in (*TFL, *PLLM):
            engine = load_script(script).performance
            invalid = [None, {}, {**FX, 'source': 'https://example.invalid'},
                       {**FX, 'date': 'tomorrow'}, {**FX, 'date': '2030-01-01'},
                       {**FX, 'retrieved_at': '2026-10-26T08:00:00'}]
            invalid += [{**FX, 'rates': {'USD': value}} for value in (0, -1, True, 'NaN', 'Infinity')]
            for fx in invalid:
                with self.subTest(fx=fx), self.assertRaisesRegex(RuntimeError, 'BCE invalide'):
                    engine.openrouter_eur_prices(0, 0, fx)

    def test_tfl_and_pllm_preserve_native_decimal_boundary(self):
        fx = {**FX, 'rates': {'USD': '1'}}
        for script in (*TFL, *PLLM):
            module = load_script(script)
            prices = {
                'input_price': 0.049999999999999996,
                'output_price': 0.25,
                'base_pricing_usd_per_million_tokens': {
                    'input': '0.05000000', 'output': '0.25000000'
                },
            }
            self.assertEqual(module.performance.native_openrouter_prices(prices),
                             ('0.05000000', '0.25000000'))
            prices['input_price'] = 0.051
            with self.assertRaisesRegex(RuntimeError, 'Prix OpenRouter natifs'):
                module.performance.native_openrouter_prices(prices)
        for script in TFL:
            module = load_script(script)
            def raw(name, price):
                return {'id': name, 'context_length': 1_000_000,
                        'reasoning': {'supported_efforts': ['medium']},
                        'pricing': {'prompt': price, 'completion': price}}
            rows, excluded = module.build_openrouter_rows({'data': [
                    raw('boundary', '0.0000001'), raw('over', '0.00000010000000000000001')]}, exchange_rates=fx)
            self.assertEqual([r['id'] for r in rows], ['boundary'])
            self.assertEqual(excluded[0]['id'], 'over')
        for script in PLLM:
            module = load_script(script)
            candidate = row('over', 'openrouter')
            candidate.update(input_price=.2, output_price=.2,
                             base_pricing_usd_per_million_tokens={'input': '0.20000000000000001', 'output': '0.20000000000000001'})
            with self.assertRaisesRegex(RuntimeError, '0.10 €/M'):
                module.catalog_candidate(candidate, 'openrouter', 1, 'date', exchange_rates=fx)

    def test_fetch_bce_requires_unambiguous_usd_and_dates(self):
        engine = load_script(TFL[0]).performance
        xml = b'<Envelope><Cube><Cube time="2026-10-23"><Cube currency="USD" rate="2.5"/></Cube></Cube></Envelope>'
        with patch.object(engine.urllib.request, 'urlopen', return_value=io.BytesIO(xml)):
            rates = engine.fetch_eur_rates()
        self.assertEqual(rates['rates']['USD'], '2.5')
        self.assertEqual(rates['date'], '2026-10-23')
        for raw in (b'bad xml', xml.replace(b'USD', b'CNY'),
                    xml.replace(b'rate="2.5"', b'rate="0"'),
                    xml.replace(b'</Cube></Cube>', b'<Cube currency="USD" rate="2.6"/></Cube></Cube>')):
            with patch.object(engine.urllib.request, 'urlopen', return_value=io.BytesIO(raw)), self.assertRaises(RuntimeError):
                engine.fetch_eur_rates()

    def test_pllm_recalculates_old_catalog_and_forced_candidate(self):
        for script in PLLM:
            module = load_script(script)
            candidate = row('paid', 'openrouter')
            candidate.update(input_price=.2, output_price=.2, average_eur=0)
            fx = {**FX, 'rates': {'USD': '0.5'}}
            with self.assertRaisesRegex(RuntimeError, '0.10 €/M'):
                module.catalog_candidate(candidate, 'openrouter', 1, 'old', exchange_rates=fx)
            with patch.object(module, 'load_tfl_catalog', return_value={'openrouter': {'models': [candidate]}}), \
                    patch.object(module.performance, 'fetch_eur_rates', return_value=fx), \
                    patch.object(module, 'get', return_value={'data': [{'id': 'over', 'context_length': 1_000_000,
                        'pricing': {'prompt': '0.0000002', 'completion': '0.0000002'}}]}), \
                    self.assertRaisesRegex(RuntimeError, 'forcé non admissible'):
                module.candidates_for({'mode': 'mode5', 'candidate_exclusions': []}, 'paid', None,
                                      {'rank': 1}, key='offline')

    def test_tfl_rate_failure_preserves_reports(self):
        import test_tfl_opencode_catalog as fixtures
        from pathlib import Path
        import tempfile
        from contextlib import ExitStack
        for script in TFL:
            module = load_script(script)
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp, ExitStack() as stack:
                output = Path(tmp)
                fixtures.GeneralOpenCodeTests().setup_main(module, output, stack)
                for name in ('tfl.json', 'tfl.md'):
                    (output / name).write_text('rapport préservé')
                fetch = stack.enter_context(patch.object(module.performance, 'fetch_eur_rates', side_effect=RuntimeError('BCE indisponible')))
                stack.enter_context(patch('sys.stderr', new_callable=io.StringIO))
                self.assertEqual(module.main(), 1)
                fetch.assert_called_once_with(timeout=1)
                self.assertTrue(all((output / n).read_text() == 'rapport préservé' for n in ('tfl.json', 'tfl.md')))


if __name__ == '__main__':
    unittest.main()
