"""EntityMemory storing structured knowledge about people, places, and objects."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


@dataclass
class Entity:
    name: str
    entity_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)


class EntityMemory(BaseMemory):
    """Entity Memory storing attributes and profiles of named entities."""

    def __init__(self):
        super().__init__(MemoryType.ENTITY)
        self._entities: Dict[str, MemoryEntry] = {}

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._entities[key.lower()] = entry
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for k, e in self._entities.items() if query.lower() in k]
        return results[:top_k]

    def clear(self) -> None:
        self._entities.clear()
