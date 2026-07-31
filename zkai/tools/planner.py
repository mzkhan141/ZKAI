"""ToolPlanner for decomposing user queries into multi-step tool calls."""

from typing import Any, Dict, List
from zkai.tools.base import ToolRegistry


class ToolPlanner:
    """Decomposes goal instructions into tool execution plans."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def plan_tools(self, goal: str) -> List[Dict[str, Any]]:
        tools = self.registry.list_tools()
        if not tools:
            return []
        return [{"tool": tools[0].name, "arguments": {"query": goal}}]
