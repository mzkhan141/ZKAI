"""AutonomousExecutor running self-directed agent loops with error recovery."""

from typing import Any, Optional
from zkai.agent.goal import Goal, GoalManager
from zkai.agent.planner import AgentPlanner
from zkai.agent.executor import AgentExecutor
from zkai.agent.verifier import AgentVerifier
from zkai.tools.base import ToolRegistry
from zkai.core.logger import get_logger

logger = get_logger("agent.autonomous")


class AutonomousExecutor:
    """Orchestrates autonomous goal decomposition, planning, tool execution, and retry recovery."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.goal_manager = GoalManager()
        self.planner = AgentPlanner()
        self.executor = AgentExecutor(tool_registry)
        self.verifier = AgentVerifier()

    def run_goal(self, goal_description: str, max_iterations: int = 15) -> Any:
        logger.info(f"Starting autonomous execution for goal: '{goal_description}'")
        goal = self.goal_manager.create_goal(title=goal_description, description=goal_description)
        plan = self.planner.create_plan(goal)
        history = self.executor.execute_plan(plan)
        return history
