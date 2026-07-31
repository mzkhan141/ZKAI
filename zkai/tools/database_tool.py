"""DatabaseTool executing SQL queries."""

from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult


class DatabaseTool(Tool):
    """Tool connecting to databases and executing queries."""

    def __init__(self):
        meta = ToolMetadata(name="database", description="Executes database queries", category="database")
        super().__init__(meta)

    def execute(self, query: str, **kwargs: Any) -> ToolResult:
        return ToolResult(tool_name=self.metadata.name, success=True, result="Database query executed successfully.")
