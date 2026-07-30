"""Main Agent Orchestrator combining LLM, Tools, Memory, and Autonomous Execution."""

from typing import Any, Optional
from zkai.agent.autonomous import AutonomousExecutor
from zkai.tools.base import ToolRegistry
from zkai.memory.manager import MemoryManager
from zkai.core.logger import get_logger

logger = get_logger("agent")


class Agent:
    """Master Agent class orchestrating autonomous goal execution and tool interactions."""

    def __init__(self, tool_registry: Optional[ToolRegistry] = None, memory: Optional[MemoryManager] = None):
        self.tools = tool_registry or ToolRegistry()
        self.memory = memory or MemoryManager()
        self.autonomous_executor = AutonomousExecutor(self.tools)

    def run(self, goal: str) -> Any:
        """Executes a high-level goal autonomously."""
        logger.info(f"Agent running goal: '{goal}'")
        return self.autonomous_executor.run_goal(goal)
