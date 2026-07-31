"""Agent Tool Selection wrapper."""

from typing import Optional
from zkai.tools.base import ToolRegistry, ToolSelector, ToolContext, Tool


class AgentToolSelector:
    """Wrapper selecting best tool for agent tasks."""

    def __init__(self, registry: ToolRegistry):
        self.selector = ToolSelector(registry)

    def select(self, task_description: str) -> Optional[Tool]:
        ctx = ToolContext(user_query=task_description)
        return self.selector.select_best_tool(ctx)
