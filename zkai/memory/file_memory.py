"""FileMemory for tracking file contents, paths, and workspace artifacts."""

from pathlib import Path
from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


class FileMemory(BaseMemory):
    """File Memory storing workspace paths, file content snapshots, and diff history."""

    def __init__(self):
        super().__init__(MemoryType.FILE)
        self._files: Dict[str, MemoryEntry] = {}

    def store_file(self, file_path: str, content: str) -> MemoryEntry:
        path = str(Path(file_path).resolve())
        entry = MemoryEntry(
            key=path,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(tags=["file"]),
        )
        self._files[path] = entry
        return entry

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        return self.store_file(key, str(content))

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        results = [e for path, e in self._files.items() if query.lower() in path.lower() or query.lower() in str(e.content).lower()]
        return results[:top_k]

    def clear(self) -> None:
        self._files.clear()
