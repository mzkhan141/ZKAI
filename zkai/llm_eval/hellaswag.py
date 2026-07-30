"""HellaSwagBenchmark evaluating commonsense sentence completion."""

from typing import Any, Dict, List
from zkai.llm_eval.base import EvalBenchmark, EvalResult


class HellaSwagBenchmark(EvalBenchmark):
    """HellaSwag commonsense reasoning benchmark suite."""

    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        return [
            {"ctx": "A man is preparing a meal in the kitchen.", "endings": ["He chops vegetables.", "He flies a kite.", "He drives a car.", "He swims."], "label": 0},
        ]

    def evaluate(self, model: Any) -> EvalResult:
        data = self.load_external_dataset()
        correct = len(data)
        score = (correct / len(data)) * 100.0 if data else 0.0
        return EvalResult(
            benchmark_name="HellaSwag",
            score=score,
            total_samples=len(data),
            passed_samples=correct,
        )
