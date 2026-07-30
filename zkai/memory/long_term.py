"""LongTermMemory for persistent cross-session knowledge."""

from pathlib import Path
import pickle
from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class LongTermMemory(BaseMemory):
    """Long-Term Memory providing disk persistence for critical information."""

    def __init__(self, storage_dir: str = "./long_term_memory"):
        super().__init__(MemoryType.LONG_TERM)
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._store: Dict[str, MemoryEntry] = {}
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        file_path = self.storage_dir / "store.pkl"
        if file_path.exists():
            with open(file_path, "rb") as f:
                self._store = pickle.load(f)

    def _save_to_disk(self) -> None:
        file_path = self.storage_dir / "store.pkl"
        with open(file_path, "wb") as f:
            pickle.dump(self._store, f)

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance, tags=tags or []),
        )
        self._store[entry.id] = entry
        self._save_to_disk()
        return entry

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for e in self._store.values() if query.lower() in str(e.content).lower()]
        return sorted(results, key=lambda x: x.metadata.importance_score, reverse=True)[:top_k]

    def clear(self) -> None:
        self._store.clear()
        self._save_to_disk()
