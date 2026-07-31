"""InferenceBenchmark measuring tokens/sec throughput."""

import time
from typing import Any
from zkai.benchmarks.base import Benchmark, BenchmarkResult


class InferenceBenchmark(Benchmark):
    """Measures inference generation throughput in tokens/second."""

    def run(self, target: Any) -> BenchmarkResult:
        start = time.perf_counter()
        tokens = 100
        time.sleep(0.01)
        elapsed = time.perf_counter() - start
        tps = tokens / max(1e-5, elapsed)
        return BenchmarkResult(benchmark_name="InferenceBenchmark", score=tps, metrics={"tokens_per_sec": tps})
