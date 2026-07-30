"""DatasetCache layer for caching dataset items in memory or disk."""

from pathlib import Path
import pickle
from typing import Any, Dict, Optional


class DatasetCache:
    """Multi-level memory/disk caching layer for pre-processed datasets."""

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[int, Any] = {}

    def get(self, idx: int) -> Optional[Any]:
        if idx in self._memory_cache:
            return self._memory_cache[idx]
        if self.cache_dir:
            file_path = self.cache_dir / f"{idx}.pkl"
            if file_path.exists():
                data = pickle.loads(file_path.read_bytes())
                self._memory_cache[idx] = data
                return data
        return None

    def set(self, idx: int, value: Any) -> None:
        self._memory_cache[idx] = value
        if self.cache_dir:
            file_path = self.cache_dir / f"{idx}.pkl"
            file_path.write_bytes(pickle.dumps(value))
