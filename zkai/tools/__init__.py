"""Plugin and Tool Architecture for ZKAI."""

from zkai.tools.auto_select import AutomaticToolSelection
from zkai.tools.base import (
    Tool,
    ToolContext,
    ToolMetadata,
    ToolPermission,
    ToolRegistry,
    ToolResult,
    ToolScorer,
    ToolSelector,
)
from zkai.tools.browser_tool import BrowserTool
from zkai.tools.calculator_tool import CalculatorTool
from zkai.tools.database_tool import DatabaseTool
from zkai.tools.executor import ToolExecutor
from zkai.tools.git_tool import GitTool
from zkai.tools.permissions import PermissionManager
from zkai.tools.planner import ToolPlanner
from zkai.tools.python_tool import PythonTool
from zkai.tools.schema import SchemaGenerator
from zkai.tools.search_tool import SearchTool
from zkai.tools.terminal_tool import TerminalTool
from zkai.tools.vision_tool import VisionTool

__all__ = [
    "Tool",
    "ToolMetadata",
    "ToolContext",
    "ToolPermission",
    "ToolResult",
    "ToolRegistry",
    "ToolScorer",
    "ToolSelector",
    "PythonTool",
    "BrowserTool",
    "VisionTool",
    "SearchTool",
    "TerminalTool",
    "CalculatorTool",
    "DatabaseTool",
    "GitTool",
    "ToolExecutor",
    "ToolPlanner",
    "AutomaticToolSelection",
    "SchemaGenerator",
    "PermissionManager",
]
