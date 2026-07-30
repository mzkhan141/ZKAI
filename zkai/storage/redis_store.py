"""RedisStore distributed cache and memory store interface with native fallback."""

from typing import Any, Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("storage.redis")

try:
    import redis
except ImportError:
    redis = None


class RedisStore:
    """Distributed Redis memory cache and state store."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db) if redis else None
        self._fallback_store: Dict[str, str] = {}

    def set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        if self.client:
            self.client.set(key, value, ex=ex)
        else:
            self._fallback_store[key] = value

    def get(self, key: str) -> Optional[str]:
        if self.client:
            res = self.client.get(key)
            return res.decode("utf-8") if isinstance(res, bytes) else res
        return self._fallback_store.get(key)
