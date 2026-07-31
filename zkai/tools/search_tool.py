"""SearchTool performing internet searches."""

import asyncio
from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult
from zkai.internet.search_engine import SearchEngine


from zkai.core.logger import get_logger

logger = get_logger("tools.search")


class SearchTool(Tool):
    """Tool executing internet web search queries."""

    def __init__(self):
        meta = ToolMetadata(name="search", description="Searches the web for latest information and papers", category="search")
        super().__init__(meta)
        self.engine = SearchEngine()

    def execute(self, query: str, **kwargs: Any) -> ToolResult:
        try:
            results = asyncio.run(self.engine.search(query))
            return ToolResult(tool_name=self.metadata.name, success=True, result=results)
        except Exception as e:
            logger.error(f"SearchTool execution failed for '{query}': {e}")
            return ToolResult(tool_name=self.metadata.name, success=False, result=[], error=str(e))
