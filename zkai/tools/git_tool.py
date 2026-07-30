"""GitTool running git operations."""

import subprocess
from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult


class GitTool(Tool):
    """Tool running git commands."""

    def __init__(self):
        meta = ToolMetadata(name="git", description="Executes git operations", category="vcs")
        super().__init__(meta)

    def execute(self, git_args: str, **kwargs: Any) -> ToolResult:
        res = subprocess.run(f"git {git_args}", shell=True, capture_output=True, text=True)
        return ToolResult(
            tool_name=self.metadata.name,
            success=(res.returncode == 0),
            result=res.stdout if res.returncode == 0 else res.stderr,
            error=res.stderr if res.returncode != 0 else None,
        )
