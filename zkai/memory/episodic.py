"""EpisodicMemory storing temporal event experiences."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


@dataclass
class EventEpisode:
    """An event episode with temporal and situational context."""
    action: str
    outcome: str
    timestamp: datetime = datetime.now()


class EpisodicMemory(BaseMemory):
    """Episodic Memory storing past interactions as event timelines."""

    def __init__(self):
        super().__init__(MemoryType.EPISODIC)
        self._episodes: List[MemoryEntry] = []

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._episodes.append(entry)
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        matches = [e for e in self._episodes if query.lower() in str(e.content).lower()]
        return matches[-top_k:]

    def clear(self) -> None:
        self._episodes.clear()
