"""Contrôles hors ligne du seuil PLLM dans les deux distributions."""

import copy
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = (
    ROOT / "skills/pllm/scripts/evaluate.py",
    ROOT / "plugins/pllm/skills/pllm/scripts/evaluate.py",
)


class PllmTtftTests(unittest.TestCase):
    def evaluate(self, script, ttft, throughput=20, quota_error=False):
        spec = importlib.util.spec_from_file_location("pllm_under_test", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        catalog = {
            "models": [
                {
                    "mode": f"mode{priority}",
                    "priority": priority,
                    "provider": provider,
                    "reasoning": "low",
                    "condition": "TTFT < 60 s ET tokens/s > 15 ET quotas valides",
                    "state": "Invalide",
                }
                for priority, provider in enumerate(
                    ("opencodego", "opencodego", "openrouter", "deepseek"), 1
                )
            ]
        }
        observed = {}
        calls = []

        def quota(model, key):
            calls.append("quota")
            if quota_error:
                raise RuntimeError("Quota indisponible")

        def benchmark(model, key, budget, metadata, session_id=None):
            calls.append("benchmark")
            model.update(ttft_seconds=ttft, tokens_per_second=throughput)
            model["performance_test"] = {"status": "completed"}
            return True

        def publish(data, **kwargs):
            observed.update(copy.deepcopy(data))

        with (
            patch.object(module, "load_memory", return_value={"policies": {}}),
            patch.object(Path, "read_text", return_value=json.dumps(catalog)),
            patch.object(module.subprocess, "run", return_value=SimpleNamespace(
                returncode=0, stdout=b"offline-fixture"
            )),
            patch.object(module, "tfl_opencode_model_at", return_value=(
                {"id": "fixture-model", "api_endpoint": "https://example.invalid", "api_protocol": "messages"},
                "fixture-date",
            )),
            patch.object(module, "quota", side_effect=quota),
            patch.object(module, "benchmark", side_effect=benchmark),
            patch.object(module, "budgets_for", return_value=(8192,)),
            patch.object(module, "remember_success") as remembered,
            patch.object(module, "publish", side_effect=publish),
            patch.object(module.signal, "signal"),
            patch.object(module.signal, "alarm"),
        ):
            module.main(forced={"mode": "mode2"})
        return module, observed["models"][1], calls, remembered.call_count

    def test_ttft_limit_is_strictly_ninety_seconds(self):
        for script in SCRIPTS:
            for ttft, expected in (
                (59.999, "Valide"), (60, "Valide"), (70.4, "Valide"),
                (89.999, "Valide"), (90, "Invalide"), (90.001, "Invalide"),
            ):
                with self.subTest(script=script, ttft=ttft):
                    _, model, calls, remembered = self.evaluate(script, ttft)
                    self.assertEqual(model["state"], expected)
                    self.assertEqual(calls, ["quota", "benchmark"])
                    self.assertEqual(remembered, int(expected == "Valide"))
                    self.assertEqual(model["condition"], "TTFT < 90 s ET tokens/s > 15 ET quotas valides")

    def test_throughput_limit_remains_strict(self):
        for script in SCRIPTS:
            for throughput, expected in ((15, "Invalide"), (15.001, "Valide")):
                with self.subTest(script=script, throughput=throughput):
                    _, model, _, _ = self.evaluate(script, 70.4, throughput)
                    self.assertEqual(model["state"], expected)

    def test_invalid_quota_prevents_the_benchmark(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                _, model, calls, remembered = self.evaluate(script, 70.4, quota_error=True)
                self.assertEqual(model["state"], "Invalide")
                self.assertEqual(calls, ["quota"])
                self.assertEqual(remembered, 0)

    def test_color_tracks_the_new_ttft_limit(self):
        for script in SCRIPTS:
            module, _, _, _ = self.evaluate(script, 70.4)
            for ttft, color in ((29.999, "🟢"), (30, "🟡"), (45, "🟠"), (89.999, "🟠"), (90, "🔴")):
                with self.subTest(script=script, ttft=ttft):
                    self.assertEqual(module.performance_color("ttft", ttft), color)


if __name__ == "__main__":
    unittest.main()
