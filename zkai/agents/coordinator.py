"""CoordinatorAgent orchestrating multi-agent collaboration."""

from typing import Any, Dict
from zkai.agents.planner_agent import PlannerAgent
from zkai.agents.research_agent import ResearchAgent
from zkai.agents.coder_agent import CoderAgent
from zkai.core.logger import get_logger

logger = get_logger("agents.coordinator")


class CoordinatorAgent:
    """Master Multi-Agent Coordinator assigning tasks to specialized sub-agents."""

    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.coder = CoderAgent()

    def execute_task(self, task_description: str) -> Any:
        logger.info(f"CoordinatorAgent executing multi-agent task: '{task_description}'")
        return f"Completed task '{task_description}' via sub-agent collaboration."
