"""Function Calling and Tool Calling parsing structures."""

from dataclasses import dataclass, field
import json
from typing import Any, Dict, Optional


@dataclass
class ToolCall:
    """Structured Tool Call invocation parsed from LLM output."""
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    call_id: str = ""


class FunctionRegistry:
    """Registry exposing python functions for tool call binding."""

    def __init__(self):
        self._functions: Dict[str, Any] = {}

    def register(self, name: str, func: Any) -> None:
        self._functions[name] = func

    def call(self, name: str, kwargs: Dict[str, Any]) -> Any:
        if name in self._functions:
            return self._functions[name](**kwargs)
        raise ValueError(f"Function {name} not found in registry.")
