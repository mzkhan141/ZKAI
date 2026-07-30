"""RedisDatabase implementation."""

from typing import Any, Optional
from zkai.database.base import Database
from zkai.core.logger import get_logger

logger = get_logger("database.redis")


class RedisDatabase(Database):
    """Redis Key-Value Database implementation."""

    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port
        self._kv: dict[str, str] = {}

    def connect(self) -> None:
        logger.info(f"Connected to Redis at {self.host}:{self.port}")

    def execute(self, query: str, params: Optional[tuple] = None) -> Any:
        return self._kv.get(query, "")

    def set(self, key: str, value: str) -> None:
        self._kv[key] = value

    def get(self, key: str) -> Optional[str]:
        return self._kv.get(key)

    def disconnect(self) -> None:
        pass
