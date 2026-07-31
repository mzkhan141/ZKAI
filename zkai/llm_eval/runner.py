"""EvalRunner orchestrating benchmark suite runs over target models."""

from typing import Any, List, Optional
from zkai.llm_eval.base import EvalBenchmark, EvalResult
from zkai.llm_eval.mmlu import MMLUBenchmark
from zkai.llm_eval.gsm8k import GSM8KBenchmark
from zkai.llm_eval.humaneval import HumanEvalBenchmark
from zkai.llm_eval.arc import ARCBenchmark
from zkai.llm_eval.truthfulqa import TruthfulQABenchmark
from zkai.llm_eval.bbh import BBHBenchmark
from zkai.llm_eval.hellaswag import HellaSwagBenchmark
from zkai.llm_eval.agentbench import AgentBenchBenchmark
from zkai.core.logger import get_logger

logger = get_logger("llm_eval.runner")


class EvalRunner:
    """Orchestrator running comprehensive benchmark suites."""

    def __init__(self, benchmarks: Optional[List[EvalBenchmark]] = None):
        self.benchmarks = benchmarks or [
            MMLUBenchmark(),
            GSM8KBenchmark(),
            HumanEvalBenchmark(),
            ARCBenchmark(),
            TruthfulQABenchmark(),
            BBHBenchmark(),
            HellaSwagBenchmark(),
            AgentBenchBenchmark(),
        ]

    def run_all(self, model: Any) -> List[EvalResult]:
        """Runs all configured benchmark suites across target model."""
        logger.info(f"Initiating evaluation runner across {len(self.benchmarks)} benchmarks...")
        results = []
        for bench in self.benchmarks:
            res = bench.evaluate(model)
            results.append(res)
            logger.info(f"Completed benchmark '{res.benchmark_name}' - Score: {res.score:.2f}% ({res.passed_samples}/{res.total_samples})")
        return results
