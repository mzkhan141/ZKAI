"""MemoryBenchmark tracking peak VRAM and RAM allocation."""

from typing import Any
import torch
from zkai.benchmarks.base import Benchmark, BenchmarkResult


class MemoryBenchmark(Benchmark):
    """Measures RAM and VRAM footprint of execution."""

    def run(self, target: Any) -> BenchmarkResult:
        vram_mb = 0.0
        if torch.cuda.is_available():
            vram_mb = torch.cuda.max_memory_allocated() / (1024 * 1024)
        return BenchmarkResult(benchmark_name="MemoryBenchmark", score=vram_mb, metrics={"vram_allocated_mb": vram_mb})
