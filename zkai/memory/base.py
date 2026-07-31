"""Base Memory Protocol, Memory Entry, and Metadata structures."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional
from zkai.core.types import MemoryType


@dataclass
class MemoryMetadata:
    """Metadata attached to stored memory entries."""
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    importance_score: float = 1.0
    decay_factor: float = 0.05
    tags: List[str] = field(default_factory=list)


@dataclass
class MemoryEntry:
    """Individual unit of stored memory across ZKAI memory subsystems."""
    key: str
    content: Any
    memory_type: MemoryType
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
    vector_embedding: Optional[List[float]] = None


class BaseMemory(ABC):
    """Abstract Base Class defining standard memory interface."""

    def __init__(self, memory_type: MemoryType):
        self.memory_type = memory_type

    @abstractmethod
    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        pass

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
