"""Response Generation Data Containers."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.language_model.function_calling import ToolCall


@dataclass
class CompletionResult:
    """Detailed completion response container."""
    text: str
    tokens_generated: int = 0
    finish_reason: str = "stop"
    tool_calls: List[ToolCall] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
