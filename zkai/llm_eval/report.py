"""EvalReport generating Markdown reports for LLM evaluation benchmark results."""

from typing import List
from zkai.llm_eval.base import EvalResult


class EvalReport:
    """Generates structured Markdown reports from benchmark run results."""

    def generate_report(self, results: List[EvalResult], model_name: str = "ZKAI Model") -> str:
        lines = [
            f"# ZKAI LLM Benchmark Evaluation Report",
            f"**Model Name**: {model_name}",
            "",
            "| Benchmark | Score (%) | Passed / Total | Subcategories |",
            "|---|---|---|---|",
        ]

        total_passed = 0
        total_samples = 0

        for r in results:
            total_passed += r.passed_samples
            total_samples += r.total_samples
            sub_str = ", ".join([f"{k}: {v:.1f}%" for k, v in r.subcategories.items()]) if r.subcategories else "N/A"
            lines.append(f"| {r.benchmark_name} | {r.score:.2f}% | {r.passed_samples} / {r.total_samples} | {sub_str} |")

        overall_score = (total_passed / total_samples * 100.0) if total_samples > 0 else 0.0
        lines.extend([
            "",
            f"**Overall Aggregate Score**: {overall_score:.2f}%",
        ])

        return "\n".join(lines)
