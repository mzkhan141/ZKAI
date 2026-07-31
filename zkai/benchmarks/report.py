"""ReportGenerator generating formatted benchmark reports."""

from typing import List
from zkai.benchmarks.base import BenchmarkResult


class ReportGenerator:
    """Generates markdown or HTML benchmark summary reports."""

    def generate_report(self, results: List[BenchmarkResult]) -> str:
        lines = ["# ZKAI Benchmark Summary Report", ""]
        lines.append("| Benchmark | Score | Timestamp |")
        lines.append("|---|---|---|")
        for r in results:
            lines.append(f"| {r.benchmark_name} | {r.score:.4f} | {r.timestamp} |")
        return "\n".join(lines)
