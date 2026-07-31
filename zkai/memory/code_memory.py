"""CodeMemory for code snippets, functions, errors, and solution patterns."""

from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class CodeMemory(BaseMemory):
    """Code Memory storing functions, classes, error solutions, and code patterns."""

    def __init__(self):
        super().__init__(MemoryType.CODE)
        self._snippets: Dict[str, MemoryEntry] = {}

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or ["code"]),
        )
        self._snippets[key] = entry
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for k, e in self._snippets.items() if query.lower() in k.lower() or query.lower() in str(e.content).lower()]
        return results[:top_k]

    def clear(self) -> None:
        self._snippets.clear()
