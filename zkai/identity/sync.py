"""IdentitySynchronizer and SessionBinder for ZKAI identity management."""

from typing import Dict, Optional
from zkai.identity.identity import Identity
from zkai.session.session import AISession
from zkai.core.logger import get_logger

logger = get_logger("identity.sync")


class IdentitySynchronizer:
    """Synchronizes identity profiles across distributed cluster nodes."""

    def __init__(self):
        self._identities: Dict[str, Identity] = {}

    def sync_identity(self, identity: Identity) -> None:
        self._identities[identity.identity_id] = identity
        logger.info(f"Synchronized identity '{identity.name}' across cluster")

    def get_identity(self, identity_id: str) -> Optional[Identity]:
        return self._identities.get(identity_id)


class SessionBinder:
    """Binds persistent AISession instances to authenticated Identities."""

    def __init__(self):
        self._bindings: Dict[str, str] = {}  # session_id -> identity_id

    def bind(self, session: AISession, identity: Identity) -> None:
        self._bindings[session.session_id] = identity.identity_id
        logger.info(f"Bound AISession '{session.session_id}' to Identity '{identity.name}'")

    def get_identity_id(self, session_id: str) -> Optional[str]:
        return self._bindings.get(session_id)
