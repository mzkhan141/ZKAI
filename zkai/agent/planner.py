"""Planner and DecisionEngine for decomposing goals into planned actions."""

from typing import List
from zkai.agent.goal import Goal
from zkai.agent.plan import Plan, Action
from zkai.core.logger import get_logger

logger = get_logger("agent.planner")


class DecisionEngine:
    """Evaluates state observations and makes decision choices."""

    def decide_next_action(self, observation: str) -> str:
        return "continue"


class AgentPlanner:
    """Decomposes goal specifications into ordered action plans."""

    def __init__(self):
        self.decision_engine = DecisionEngine()

    def create_plan(self, goal: Goal) -> Plan:
        logger.info(f"Creating execution plan for goal: {goal.title}")
        plan = Plan(goal_id=goal.id)
        # Add actions
        plan.actions.append(Action(tool_name="search", arguments={"query": goal.title}))
        return plan
