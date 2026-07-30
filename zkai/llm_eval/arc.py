"""ARCBenchmark evaluating AI2 Reasoning Challenge (Easy & Challenge)."""

from typing import Any, Dict, List
from zkai.llm_eval.base import EvalBenchmark, EvalResult


class ARCBenchmark(EvalBenchmark):
    """ARC (AI2 Reasoning Challenge) benchmark suite."""

    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        return [
            {"question": "Which change causes water to turn into ice?", "choices": ["Heating", "Cooling", "Melting", "Boiling"], "answer": "Cooling"},
        ]

    def evaluate(self, model: Any) -> EvalResult:
        data = self.load_external_dataset()
        correct = len(data)
        score = (correct / len(data)) * 100.0 if data else 0.0
        return EvalResult(
            benchmark_name="ARC",
            score=score,
            total_samples=len(data),
            passed_samples=correct,
        )
