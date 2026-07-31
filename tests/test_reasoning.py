"""Unit tests for Reasoning Engine subsystem."""

import pytest
from zkai.reasoning import ConsensusReasoning, GraphReasoner, PlanningEngine, RecursiveReasoner, TreeSearch


def test_tree_search():
    ts = TreeSearch()
    root = ts.search("solve riddle", depth=2)
    assert root.state == "solve riddle"
    assert len(root.children) == 1


test_tree_search()


def test_consensus_reasoning():
    cr = ConsensusReasoning()
    res = cr.aggregate(["ans_a", "ans_a", "ans_b"])
    assert res == "ans_a"


def test_recursive_reasoner():
    rr = RecursiveReasoner()
    sol = rr.solve_recursively("complex_problem")
    assert "complex_problem" in sol
