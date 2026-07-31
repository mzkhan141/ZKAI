"""Tool Abstract Base Class, ToolRegistry, ToolScorer, and ToolSelector framework."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("tools.base")


@dataclass
class ToolMetadata:
    name: str
    description: str
    category: str = "general"
    version: str = "1.0.0"


@dataclass
class ToolContext:
    user_query: str
    active_environment: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolPermission:
    requires_approval: bool = False
    allowed: bool = True


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None


class Tool(ABC):
    """Abstract Base Class for all ZKAI Tools and Plugins."""

    def __init__(self, metadata: ToolMetadata):
        self.metadata = metadata
        self.permission = ToolPermission()

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> ToolResult:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> ToolResult:
        return self.execute(*args, **kwargs)


class ToolRegistry:
    """Registry maintaining available tools."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.metadata.name] = tool
        logger.info(f"Registered tool: '{tool.metadata.name}'")

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolMetadata]:
        return [t.metadata for t in self._tools.values()]


class ToolScorer:
    """Scores relevance of candidate tools for a user query context."""

    def score(self, tool: Tool, context: ToolContext) -> float:
        query_words = set(context.user_query.lower().split())
        desc_words = set(tool.metadata.description.lower().split())
        name_words = set(tool.metadata.name.lower().split("_"))

        overlap = len(query_words.intersection(desc_words.union(name_words)))
        return float(overlap)


class ToolSelector:
    """Automatically selects the best tool matching query requirements."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.scorer = ToolScorer()

    def select_best_tool(self, context: ToolContext) -> Optional[Tool]:
        tools = list(self.registry._tools.values())
        if not tools:
            return None

        scored = [(t, self.scorer.score(t, context)) for t in tools]
        scored.sort(key=lambda item: item[1], reverse=True)
        best_tool, best_score = scored[0]
        if best_score > 0:
            return best_tool
        return tools[0]
