"""AutomaticToolSelection engine."""

from typing import Optional
from zkai.tools.base import Tool, ToolContext, ToolRegistry, ToolSelector


class AutomaticToolSelection:
    """Wraps ToolSelector for query context tool matching."""

    def __init__(self, registry: ToolRegistry):
        self.selector = ToolSelector(registry)

    def select(self, query: str) -> Optional[Tool]:
        ctx = ToolContext(user_query=query)
        return self.selector.select_best_tool(ctx)
