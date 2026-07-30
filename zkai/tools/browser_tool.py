"""BrowserTool automating web page navigation."""

import asyncio
from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult
from zkai.browser.search import BrowserSearch


from zkai.core.logger import get_logger

logger = get_logger("tools.browser")


class BrowserTool(Tool):
    """Tool automating web browsing and web searching."""

    def __init__(self):
        meta = ToolMetadata(name="browser", description="Opens websites and searches the web", category="web")
        super().__init__(meta)
        self.search_engine = BrowserSearch()

    def execute(self, query_or_url: str, **kwargs: Any) -> ToolResult:
        try:
            res = asyncio.run(self.search_engine.search(query_or_url))
            return ToolResult(tool_name=self.metadata.name, success=True, result=res)
        except Exception as e:
            logger.error(f"BrowserTool execution failed for '{query_or_url}': {e}")
            return ToolResult(tool_name=self.metadata.name, success=False, result="", error=str(e))
