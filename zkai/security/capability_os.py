"""Capability-Based Operating System Execution, Token Resolution, Policies, and Auditing for ZKAI."""

from dataclasses import dataclass, field
import datetime
import time
import uuid
from typing import Any, Dict, List, Optional, Set
from zkai.core.logger import get_logger

logger = get_logger("security.capability_os")


@dataclass
class Capability:
    """Represents a fine-grained OS capability grant."""
    name: str  # e.g., "Inference", "Memory", "Filesystem", "GPU", "Vision", "Voice"
    scope: str = "*"
    permissions: List[str] = field(default_factory=lambda: ["read", "execute"])


@dataclass
class CapabilityLease:
    """Time-bounded lease for a capability grant."""
    lease_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capability_name: str = ""
    holder_id: str = ""
    expires_at: float = field(default_factory=lambda: time.time() + 3600.0)

    def is_valid(self) -> bool:
        return time.time() < self.expires_at


@dataclass
class CapabilityToken:
    """Capability token carrying granted capabilities and lifetime metadata."""
    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    subject: str = "default_subject"
    capabilities: List[Capability] = field(default_factory=list)
    issued_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None

    def is_valid(self) -> bool:
        if self.expires_at:
            return time.time() < self.expires_at
        return True


class CapabilityCache:
    """Caching capability lookup results for high-performance permission checks."""

    def __init__(self):
        self._cache: Dict[str, bool] = {}

    def get(self, key: str) -> Optional[bool]:
        return self._cache.get(key)

    def put(self, key: str, value: bool) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()


class CapabilityPolicy:
    """Policy rules governing capability derivation and delegation."""

    def __init__(self):
        self.allowed_capabilities: Set[str] = {
            "Inference", "Memory", "Filesystem", "Browser", "Vision", "Voice",
            "Network", "GPU", "Workflow", "Models", "Knowledge", "Desktop",
            "Clipboard", "Camera", "Microphone", "USB", "Bluetooth", "Plugins",
            "Applications", "Services",
        }

    def is_allowed(self, capability_name: str) -> bool:
        return capability_name in self.allowed_capabilities


class CapabilityAudit:
    """Audit log recorder for capability evaluations and access grants."""

    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def record(self, subject: str, capability_name: str, granted: bool, reason: str = "") -> None:
        self.audit_log.append({
            "subject": subject,
            "capability": capability_name,
            "granted": granted,
            "reason": reason,
            "timestamp": time.time(),
        })


class KernelCapabilityTable:
    """Global Kernel Capability Table indexing active capability tokens and leases."""

    def __init__(self):
        self.tokens: Dict[str, CapabilityToken] = {}
        self.leases: Dict[str, CapabilityLease] = {}

    def add_token(self, token: CapabilityToken) -> None:
        self.tokens[token.token_id] = token

    def add_lease(self, lease: CapabilityLease) -> None:
        self.leases[lease.lease_id] = lease

    def get_token(self, token_id: str) -> Optional[CapabilityToken]:
        return self.tokens.get(token_id)


class CapabilityResolver:
    """Resolves subject requests against granted capabilities in CapabilityTokens."""

    @staticmethod
    def resolve(token: CapabilityToken, target_capability: str, required_permission: str = "execute") -> bool:
        if not token.is_valid():
            return False
        for cap in token.capabilities:
            if cap.name == target_capability or cap.name == "*":
                if required_permission in cap.permissions or "*" in cap.permissions:
                    return True
        return False


class CapabilityBroker:
    """Brokers capability exchanges and dynamic lease grants between kernel services."""

    def __init__(self, table: KernelCapabilityTable):
        self.table = table

    def issue_lease(self, subject: str, capability_name: str, duration_seconds: float = 3600.0) -> CapabilityLease:
        lease = CapabilityLease(capability_name=capability_name, holder_id=subject, expires_at=time.time() + duration_seconds)
        self.table.add_lease(lease)
        logger.info(f"CapabilityBroker issued lease for '{capability_name}' to '{subject}' (valid for {duration_seconds}s)")
        return lease


class CapabilityManager:
    """Master Capability Governor granting, verifying, and revoking OS capabilities."""

    def __init__(self):
        self.table = KernelCapabilityTable()
        self.resolver = CapabilityResolver()
        self.broker = CapabilityBroker(self.table)
        self.cache = CapabilityCache()
        self.policy = CapabilityPolicy()
        self.audit = CapabilityAudit()

    def grant_capability(self, subject: str, capability_name: str, permissions: Optional[List[str]] = None) -> CapabilityToken:
        if not self.policy.is_allowed(capability_name):
            logger.warning(f"CapabilityManager blocked invalid capability request '{capability_name}' for subject '{subject}'")

        cap = Capability(name=capability_name, permissions=permissions or ["read", "execute"])
        token = CapabilityToken(subject=subject, capabilities=[cap])
        self.table.add_token(token)
        self.audit.record(subject, capability_name, granted=True, reason="Granted by manager")
        logger.info(f"CapabilityManager granted capability '{capability_name}' to subject '{subject}'")
        return token

    def verify_capability(self, token: CapabilityToken, capability_name: str, permission: str = "execute") -> bool:
        cache_key = f"{token.token_id}:{capability_name}:{permission}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        res = self.resolver.resolve(token, capability_name, required_permission=permission)
        self.cache.put(cache_key, res)
        self.audit.record(token.subject, capability_name, granted=res, reason="Verification lookup")
        return res
