"""Multi-tier Caching Infrastructure (In-Memory LRU, TTL, Disk Cache)."""

from abc import ABC, abstractmethod
from collections import OrderedDict
import pickle
import time
from pathlib import Path
from typing import Any, Optional, Dict
from zkai.core.logger import get_logger

logger = get_logger("cache")


class Cache(ABC):
    """Abstract Base Class for Caching interfaces."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError


class LRUCache(Cache):
    """Least Recently Used (LRU) In-Memory Cache."""

    def __init__(self, capacity: int = 128):
        self.capacity = capacity
        self._cache: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def set(self, key: str, value: Any) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()


class TTLCache(Cache):
    """Time-To-Live (TTL) In-Memory Cache with expiration handling."""

    def __init__(self, ttl_seconds: float = 300.0):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        val, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None
        return val

    def set(self, key: str, value: Any) -> None:
        expiry = time.time() + self.ttl_seconds
        self._cache[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()


class DiskCache(Cache):
    """Persistent File-based Disk Cache using pickle serialization."""

    def __init__(self, cache_dir: str = "./.zkai_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key_path(self, key: str) -> Path:
        safe_key = "".join([c if c.isalnum() else "_" for c in key])
        return self.cache_dir / f"{safe_key}.cache"

    def get(self, key: str) -> Optional[Any]:
        path = self._key_path(key)
        if not path.exists():
            return None
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Error reading disk cache key '{key}': {e}")
            return None

    def set(self, key: str, value: Any) -> None:
        path = self._key_path(key)
        try:
            with open(path, "wb") as f:
                pickle.dump(value, f)
        except Exception as e:
            logger.error(f"Error writing disk cache key '{key}': {e}")

    def delete(self, key: str) -> bool:
        path = self._key_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def clear(self) -> None:
        for file in self.cache_dir.glob("*.cache"):
            file.unlink()
