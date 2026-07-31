"""ProceduralMemory for motor skills, tool execution patterns, and routines."""

from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class ProceduralMemory(BaseMemory):
    """Procedural Memory storing step-by-step routines and skill patterns."""

    def __init__(self):
        super().__init__(MemoryType.PROCEDURAL)
        self._skills: Dict[str, MemoryEntry] = {}

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._skills[key] = entry
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for k, e in self._skills.items() if query.lower() in k.lower()]
        return results[:top_k]

    def clear(self) -> None:
        self._skills.clear()
