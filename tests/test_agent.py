"""Unit tests for zkai.agent framework."""

import pytest
from zkai.agent.agent import Agent
from zkai.agent.goal import GoalManager
from zkai.tools import ToolRegistry, PythonTool, SearchTool


def test_goal_manager():
    gm = GoalManager()
    goal = gm.create_goal("Build app", "Build a Python app")
    gm.add_subtask(goal, "Write code")
    assert len(goal.subtasks) == 1
    assert goal.subtasks[0].description == "Write code"


def test_agent_tool_registry():
    registry = ToolRegistry()
    registry.register(PythonTool())
    registry.register(SearchTool())
    assert len(registry.list_tools()) == 2


def test_agent_run():
    agent = Agent()
    res = agent.run("Search latest papers")
    assert res is not None
