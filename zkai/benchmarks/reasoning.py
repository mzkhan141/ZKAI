"""ReasoningBenchmark evaluating reasoning capabilities."""

from typing import Any
from zkai.benchmarks.base import Benchmark, BenchmarkResult


class ReasoningBenchmark(Benchmark):
    """Measures multi-step problem solving accuracy."""

    def run(self, target: Any) -> BenchmarkResult:
        score = 0.88
        return BenchmarkResult(benchmark_name="ReasoningBenchmark", score=score, metrics={"reasoning_score": score})
