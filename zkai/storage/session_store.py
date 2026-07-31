"""SessionStore for storing stateful user & agent session data."""

import uuid
from typing import Any, Dict, Optional
from zkai.storage.cache_store import CacheStore


class SessionStore:
    """Session management store persisting user interaction states."""

    def __init__(self, session_ttl_seconds: float = 7200.0):
        self.cache = CacheStore(default_ttl_seconds=session_ttl_seconds)

    def create_session(self, initial_data: Optional[Dict[str, Any]] = None) -> str:
        session_id = str(uuid.uuid4())
        data = initial_data or {}
        self.cache.set(session_id, data)
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.cache.get(session_id)

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> None:
        current = self.get_session(session_id) or {}
        current.update(updates)
        self.cache.set(session_id, current)

    def terminate_session(self, session_id: str) -> None:
        self.cache.delete(session_id)
