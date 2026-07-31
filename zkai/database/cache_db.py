"""CacheDatabase multi-level caching layer."""

from typing import Any, Optional
from zkai.core.cache import LRUCache, DiskCache


class CacheDatabase:
    """Multi-tiered database caching layer."""

    def __init__(self):
        self.lru = LRUCache(capacity=500)
        self.disk = DiskCache()

    def get(self, key: str) -> Optional[Any]:
        val = self.lru.get(key)
        if val is not None:
            return val
        val = self.disk.get(key)
        if val is not None:
            self.lru.set(key, val)
        return val

    def set(self, key: str, value: Any) -> None:
        self.lru.set(key, value)
        self.disk.set(key, value)
