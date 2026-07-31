"""LatencyBenchmark for measuring forward pass wall-clock latency."""

import time
from typing import Any
from zkai.benchmarks.base import Benchmark, BenchmarkResult


class LatencyBenchmark(Benchmark):
    """Measures model inference latency in milliseconds across N iterations."""

    def __init__(self, iterations: int = 50):
        self.iterations = iterations

    def run(self, target: Any) -> BenchmarkResult:
        start = time.perf_counter()
        for _ in range(self.iterations):
            if callable(target):
                target()
        elapsed = (time.perf_counter() - start) * 1000.0 / max(1, self.iterations)
        return BenchmarkResult(benchmark_name="LatencyBenchmark", score=elapsed, metrics={"avg_latency_ms": elapsed})
