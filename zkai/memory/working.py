"""Working Memory for active task context (bounded capacity)."""

from collections import deque
from typing import Any, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class WorkingMemory(BaseMemory):
    """Working Memory storing immediate attention items for active reasoning."""

    def __init__(self, capacity: int = 20):
        super().__init__(MemoryType.WORKING)
        self.capacity = capacity
        self._store: deque[MemoryEntry] = deque(maxlen=capacity)

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._store.append(entry)
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Retrieves items matching query substring."""
        matches = [e for e in self._store if query.lower() in str(e.content).lower() or query.lower() in e.key.lower()]
        return matches[:top_k]

    def get_all(self) -> List[MemoryEntry]:
        return list(self._store)

    def clear(self) -> None:
        self._store.clear()
