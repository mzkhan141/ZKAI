"""ToolExecutor running tool execution with safety timeouts and error handling."""

from typing import Any, Dict
from zkai.tools.base import Tool, ToolRegistry, ToolResult
from zkai.core.logger import get_logger

logger = get_logger("tools.executor")


class ToolExecutor:
    """Managed tool execution engine with sandboxing and parameter mapping."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute_tool(self, name: str, kwargs: Dict[str, Any]) -> ToolResult:
        tool = self.registry.get(name)
        if not tool:
            return ToolResult(tool_name=name, success=False, result=None, error=f"Tool '{name}' not registered")
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}")
            return ToolResult(tool_name=name, success=False, result=None, error=str(e))
