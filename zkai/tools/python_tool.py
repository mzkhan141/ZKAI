"""PythonTool executing Python code blocks."""

from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult
from zkai.coding.runner import PythonRunner


class PythonTool(Tool):
    """Tool executing python code snippets in isolated sandbox."""

    def __init__(self):
        meta = ToolMetadata(name="python", description="Executes python code snippets and scripts", category="coding")
        super().__init__(meta)
        self.runner = PythonRunner()

    def execute(self, code: str, **kwargs: Any) -> ToolResult:
        res = self.runner.run(code)
        return ToolResult(
            tool_name=self.metadata.name,
            success=(res.exit_code == 0),
            result=res.stdout if res.exit_code == 0 else res.stderr,
            error=res.stderr if res.exit_code != 0 else None,
        )
