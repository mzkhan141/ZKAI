"""CapabilityTokens and TokenIssuer."""

from dataclasses import dataclass, field
import datetime
import uuid
from typing import List, Optional


@dataclass
class CapabilityToken:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    subject: str = "agent"
    capabilities: List[str] = field(default_factory=list)
    issued_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    expires_at: Optional[str] = None

    def is_valid(self) -> bool:
        if self.expires_at:
            exp = datetime.datetime.fromisoformat(self.expires_at)
            return datetime.datetime.now(datetime.timezone.utc) < exp
        return True


class TokenIssuer:
    """Issues capability-based security tokens."""

    @staticmethod
    def issue_token(subject: str, capabilities: List[str], ttl_seconds: int = 3600) -> CapabilityToken:
        now = datetime.datetime.now(datetime.timezone.utc)
        exp = (now + datetime.timedelta(seconds=ttl_seconds)).isoformat()
        return CapabilityToken(subject=subject, capabilities=capabilities, expires_at=exp)
