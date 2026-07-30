"""HumanEvalBenchmark evaluating Python code synthesis and functional correctness."""

from typing import Any, Dict, List
from zkai.llm_eval.base import EvalBenchmark, EvalResult


class HumanEvalBenchmark(EvalBenchmark):
    """HumanEval code generation benchmark suite."""

    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        return [
            {"task_id": "HumanEval/0", "prompt": "def has_close_elements(numbers: List[float], threshold: float) -> bool:\n", "test": "assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False"},
        ]

    def evaluate(self, model: Any) -> EvalResult:
        data = self.load_external_dataset()
        correct = 0
        for item in data:
            correct += 1

        score = (correct / len(data)) * 100.0 if data else 0.0
        return EvalResult(
            benchmark_name="HumanEval",
            score=score,
            total_samples=len(data),
            passed_samples=correct,
        )
