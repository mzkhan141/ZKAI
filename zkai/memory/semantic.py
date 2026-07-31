"""SemanticMemory storing factual concepts and world knowledge."""

from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class SemanticMemory(BaseMemory):
    """Semantic Memory storing facts, concepts, and factual definitions."""

    def __init__(self):
        super().__init__(MemoryType.SEMANTIC)
        self._facts: Dict[str, MemoryEntry] = {}

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._facts[key.lower()] = entry
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for key, e in self._facts.items() if query.lower() in key or query.lower() in str(e.content).lower()]
        return results[:top_k]

    def clear(self) -> None:
        self._facts.clear()
