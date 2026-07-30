"""Tests for LLM Evaluation Benchmark Suite."""

import pytest
from zkai.llm_eval.mmlu import MMLUBenchmark
from zkai.llm_eval.gsm8k import GSM8KBenchmark
from zkai.llm_eval.humaneval import HumanEvalBenchmark
from zkai.llm_eval.arc import ARCBenchmark
from zkai.llm_eval.truthfulqa import TruthfulQABenchmark
from zkai.llm_eval.bbh import BBHBenchmark
from zkai.llm_eval.hellaswag import HellaSwagBenchmark
from zkai.llm_eval.agentbench import AgentBenchBenchmark
from zkai.llm_eval.runner import EvalRunner
from zkai.llm_eval.report import EvalReport


def test_individual_benchmarks():
    mmlu = MMLUBenchmark().evaluate(None)
    assert mmlu.benchmark_name == "MMLU"
    assert mmlu.score >= 0.0

    gsm8k = GSM8KBenchmark().evaluate(None)
    assert gsm8k.benchmark_name == "GSM8K"

    humaneval = HumanEvalBenchmark().evaluate(None)
    assert humaneval.benchmark_name == "HumanEval"


def test_eval_runner_and_report():
    runner = EvalRunner()
    results = runner.run_all(None)
    assert len(results) == 8

    report = EvalReport().generate_report(results, model_name="ZKAI LLM")
    assert "# ZKAI LLM Benchmark Evaluation Report" in report
    assert "MMLU" in report
