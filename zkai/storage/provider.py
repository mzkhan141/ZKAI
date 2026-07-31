"""StorageProvider unifying blob, object, cache, session, and analytical stores."""

from typing import Any, Dict, Optional
from zkai.storage.blob import BlobStore
from zkai.storage.object_store import ObjectStore
from zkai.storage.cache_store import CacheStore
from zkai.storage.session_store import SessionStore
from zkai.storage.duckdb_store import DuckDBStore
from zkai.storage.lmdb_store import LMDBStore
from zkai.storage.redis_store import RedisStore
from zkai.core.types import StorageBackendType
from zkai.core.logger import get_logger

logger = get_logger("storage.provider")


class StorageProvider:
    """Unified Storage Provider facade automatically selecting best available backend."""

    def __init__(self, default_backend: StorageBackendType = StorageBackendType.AUTO):
        self.default_backend = default_backend
        self.blob = BlobStore()
        self.object = ObjectStore()
        self.cache = CacheStore()
        self.session = SessionStore()
        self.duckdb = DuckDBStore()
        self.lmdb = LMDBStore()
        self.redis = RedisStore()

        logger.info(f"Initialized StorageProvider with default backend '{default_backend.value}'")

    def auto_select_backend(self, usage: str = "cache") -> Any:
        """Selects optimal backend for given usage pattern."""
        if usage == "blob":
            return self.blob
        elif usage == "object":
            return self.object
        elif usage == "session":
            return self.session
        elif usage == "analytics" and self.duckdb.conn is not None:
            return self.duckdb
        elif usage == "keyvalue" and self.lmdb.env is not None:
            return self.lmdb
        elif usage == "distributed" and self.redis.client is not None:
            return self.redis
        return self.cache
