"""CacheStore for high-performance TTL-based key caching."""

import time
from typing import Any, Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("storage.cache")


class CacheStore:
    """In-memory key-value cache store with Time-To-Live (TTL) expiration support."""

    def __init__(self, default_ttl_seconds: float = 3600.0):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Any] = {}
        self._expirations: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        self._store[key] = value
        expiration = time.time() + (ttl if ttl is not None else self.default_ttl)
        self._expirations[key] = expiration

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None

        if time.time() > self._expirations.get(key, 0.0):
            self.delete(key)
            return None

        return self._store[key]

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
        self._expirations.pop(key, None)
