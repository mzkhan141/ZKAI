"""Unit tests for Benchmark Suite subsystem."""

import pytest
from zkai.benchmarks import (
    AccuracyBenchmark,
    InferenceBenchmark,
    LatencyBenchmark,
    MemoryBenchmark,
    ReasoningBenchmark,
    ReportGenerator,
)


def test_benchmarks():
    lat = LatencyBenchmark(iterations=5).run(lambda: 1 + 1)
    assert lat.score >= 0.0

    mem = MemoryBenchmark().run(None)
    assert mem.benchmark_name == "MemoryBenchmark"

    acc = AccuracyBenchmark().run(None)
    assert acc.score > 0.9

    rep = ReportGenerator().generate_report([lat, mem, acc])
    assert "# ZKAI Benchmark Summary Report" in rep
