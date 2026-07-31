"""Identity hierarchy, Profiles, and Authentication/Authorization for ZKAI."""

from dataclasses import dataclass, field
import datetime
import uuid
from typing import Any, Dict, List, Optional
from zkai.security.tokens import TokenIssuer, CapabilityToken
from zkai.security.permissions import PermissionEngine
from zkai.core.logger import get_logger

logger = get_logger("identity")


@dataclass
class Profile:
    """User or identity preferences and settings profile."""
    name: str = "default_user"
    email: str = "user@zkai.local"
    preferences: Dict[str, Any] = field(default_factory=dict)


class Identity:
    """Base class for persistent OS identities."""

    def __init__(self, name: str, identity_type: str = "user"):
        self.identity_id: str = str(uuid.uuid4())
        self.name: str = name
        self.identity_type: str = identity_type
        self.profile: Profile = Profile(name=name)
        self.capabilities: List[str] = []
        self.created_at: str = datetime.datetime.now(datetime.timezone.utc).isoformat()


class User(Identity):
    def __init__(self, name: str):
        super().__init__(name=name, identity_type="user")


class Organization(Identity):
    def __init__(self, name: str):
        super().__init__(name=name, identity_type="organization")


class DeviceIdentity(Identity):
    def __init__(self, device_name: str):
        super().__init__(name=device_name, identity_type="device")


class AgentIdentity(Identity):
    def __init__(self, agent_name: str):
        super().__init__(name=agent_name, identity_type="agent")


class AuthenticationManager:
    """Issues and verifies authentication tokens for identities."""

    def __init__(self):
        self.token_issuer = TokenIssuer()

    def authenticate(self, identity: Identity, ttl_seconds: int = 86400) -> CapabilityToken:
        logger.info(f"Authenticated identity '{identity.name}' ({identity.identity_type})")
        return self.token_issuer.issue_token(identity.identity_id, identity.capabilities, ttl_seconds=ttl_seconds)


class AuthorizationManager:
    """Evaluates access permissions for authenticated identities."""

    def __init__(self):
        self.permission_engine = PermissionEngine()

    def authorize(self, role: str, capability: str) -> bool:
        return self.permission_engine.check_permission(role, capability)
