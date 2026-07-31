"""Tests for WorkflowEngine DAG nodes and execution runner."""

import pytest
from zkai.workflow.nodes import ActionNode, Conditional, Loop, Parallel, Merge, Retry, HumanApproval
from zkai.workflow.engine import WorkflowEngine, WorkflowRunner
from zkai.workflow.scheduler import WorkflowScheduler


def test_action_node():
    node = ActionNode("add_one", lambda x: x + 1)
    res = node.execute({"input": 10})
    assert res == 11


def test_conditional_node():
    cond = Conditional("check_positive", lambda x: x > 0, true_branch="branch_a", false_branch="branch_b")
    res_a = cond.execute({"input": 5})
    assert res_a == "branch_a"
    res_b = cond.execute({"input": -2})
    assert res_b == "branch_b"


def test_loop_node():
    body = ActionNode("inc", lambda x: x + 1)
    loop = Loop("loop_10", condition=lambda x: x < 5, body=body)
    res = loop.execute({"input": 0})
    assert res == 5


def test_retry_node():
    count = 0

    def flaky_action(x):
        nonlocal count
        count += 1
        if count < 2:
            raise ValueError("Flaky failure")
        return x * 2

    inner = ActionNode("flaky", flaky_action)
    retry_node = Retry("retry_flaky", inner, max_retries=3)
    res = retry_node.execute({"input": 4})
    assert res == 8


def test_workflow_engine_runner():
    engine = WorkflowEngine("test_workflow")
    engine.add_node(ActionNode("step1", lambda x: x + 5))
    engine.add_node(ActionNode("step2", lambda x: x * 2))

    runner = WorkflowRunner(engine)
    final_output = runner.run(10)
    assert final_output == 30
