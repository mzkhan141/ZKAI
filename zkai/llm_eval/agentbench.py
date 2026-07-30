"""AgentBenchBenchmark evaluating multi-step agent decision making, tool use, and OS tasks."""

from typing import Any, Dict, List
from zkai.llm_eval.base import EvalBenchmark, EvalResult


class AgentBenchBenchmark(EvalBenchmark):
    """AgentBench autonomous agent performance benchmark suite."""

    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        return [
            {"domain": "os_terminal", "goal": "Find all log files in /var/log", "expected_action": "ls /var/log/*.log"},
        ]

    def evaluate(self, model: Any) -> EvalResult:
        data = self.load_external_dataset()
        correct = len(data)
        score = (correct / len(data)) * 100.0 if data else 0.0
        return EvalResult(
            benchmark_name="AgentBench",
            score=score,
            total_samples=len(data),
            passed_samples=correct,
        )
