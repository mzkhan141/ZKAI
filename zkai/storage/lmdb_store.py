"""LMDBStore high-performance key-value store with native dict fallback."""

from typing import Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("storage.lmdb")

try:
    import lmdb
except ImportError:
    lmdb = None


class LMDBStore:
    """Embedded lightning memory-mapped database (LMDB) key-value store."""

    def __init__(self, path: str = "./zkai_lmdb"):
        self.path = path
        self.env = lmdb.open(path, map_size=10485760) if lmdb else None
        self._fallback_store: Dict[bytes, bytes] = {}

    def put(self, key: bytes, value: bytes) -> None:
        if self.env:
            with self.env.begin(write=True) as txn:
                txn.put(key, value)
        else:
            self._fallback_store[key] = value

    def get(self, key: bytes) -> Optional[bytes]:
        if self.env:
            with self.env.begin(write=False) as txn:
                return txn.get(key)
        return self._fallback_store.get(key)
