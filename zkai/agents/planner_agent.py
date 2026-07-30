"""PlannerAgent specialized in goal decomposition."""

from zkai.agent.planner import AgentPlanner
from zkai.agent.goal import Goal


class PlannerAgent:
    """Specialized Agent for goal analysis and subtask decomposition."""

    def __init__(self):
        self.planner = AgentPlanner()

    def create_plan(self, goal_text: str):
        goal = Goal(description=goal_text)
        return self.planner.create_plan(goal)
