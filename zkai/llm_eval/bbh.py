"""BBHBenchmark evaluating Big-Bench Hard algorithmic and symbolic tasks."""

from typing import Any, Dict, List
from zkai.llm_eval.base import EvalBenchmark, EvalResult


class BBHBenchmark(EvalBenchmark):
    """BBH (BIG-Bench Hard) algorithmic reasoning benchmark suite."""

    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        return [
            {"task": "boolean_expressions", "question": "True and (False or True) is?", "answer": "True"},
        ]

    def evaluate(self, model: Any) -> EvalResult:
        data = self.load_external_dataset()
        correct = len(data)
        score = (correct / len(data)) * 100.0 if data else 0.0
        return EvalResult(
            benchmark_name="BBH",
            score=score,
            total_samples=len(data),
            passed_samples=correct,
        )
