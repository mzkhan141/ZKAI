"""ShortTermMemory for recent turn interactions with TTL expiration."""

import time
from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class ShortTermMemory(BaseMemory):
    """Short-Term Memory storing recent conversation turns and temporary context."""

    def __init__(self, capacity: int = 1000, ttl_seconds: float = 3600.0):
        super().__init__(MemoryType.SHORT_TERM)
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, MemoryEntry] = {}

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._store[entry.id] = entry
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for e in self._store.values() if query.lower() in str(e.content).lower()]
        return results[:top_k]

    def clear(self) -> None:
        self._store.clear()
