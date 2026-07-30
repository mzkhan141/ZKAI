"""TerminalTool running shell commands."""

from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult
from zkai.coding.terminal import Terminal


class TerminalTool(Tool):
    """Tool executing terminal shell commands."""

    def __init__(self):
        meta = ToolMetadata(name="terminal", description="Executes shell terminal commands", category="system")
        super().__init__(meta)
        self.terminal = Terminal()

    def execute(self, command: str, **kwargs: Any) -> ToolResult:
        output = self.terminal.execute(command)
        return ToolResult(tool_name=self.metadata.name, success=True, result=output)
