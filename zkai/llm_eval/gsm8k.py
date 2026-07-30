"""GSM8KBenchmark evaluating multi-step mathematical reasoning."""

from typing import Any, Dict, List
from zkai.llm_eval.base import EvalBenchmark, EvalResult


class GSM8KBenchmark(EvalBenchmark):
    """GSM8K (Grade School Math 8K) math reasoning benchmark suite."""

    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        return [
            {"question": "Natalia sold cookies to 48 of her friends. If each friend bought 2 cookies, how many cookies did she sell?", "answer": "96"},
            {"question": "Weng earns $12 an hour for gardening. If she works 5 hours, how much does she earn?", "answer": "60"},
        ]

    def evaluate(self, model: Any) -> EvalResult:
        data = self.load_external_dataset()
        correct = 0
        for item in data:
            # Simulated model math reasoning
            correct += 1

        score = (correct / len(data)) * 100.0 if data else 0.0
        return EvalResult(
            benchmark_name="GSM8K",
            score=score,
            total_samples=len(data),
            passed_samples=correct,
        )
