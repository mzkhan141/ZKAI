"""Capability-based PermissionEngine, PermissionManager, ApprovalRequest, and SandboxProfile."""

from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List, Optional, Set
from zkai.core.logger import get_logger

logger = get_logger("security.permissions")

# All 21 Capability permissions required by ZKAI AI Operating System
ALL_CAPABILITIES = {
    "filesystem",
    "browser",
    "camera",
    "microphone",
    "clipboard",
    "keyboard",
    "mouse",
    "terminal",
    "email",
    "calendar",
    "network",
    "usb",
    "bluetooth",
    "contacts",
    "location",
    "notifications",
    "models",
    "memory",
    "knowledge",
    "services",
    "workflows",
}


@dataclass
class SandboxProfile:
    """Pre-configured sandbox profile restricting process execution capabilities."""
    name: str
    allowed_capabilities: Set[str] = field(default_factory=set)
    read_only_filesystem: bool = True
    network_access: bool = False


@dataclass
class ApprovalRequest:
    """Human-in-the-loop permission request for sensitive operations."""
    request_id: str
    agent_id: str
    capability: str
    reason: str
    status: str = "pending"  # pending, approved, rejected
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class PermissionAudit:
    """Audit recorder for permission evaluation requests."""

    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def record_check(self, role_or_subject: str, capability: str, granted: bool) -> None:
        self.logs.append({
            "subject": role_or_subject,
            "capability": capability,
            "granted": granted,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        })


class PermissionEngine:
    """RBAC and Capability-based Permission Engine evaluating capabilities across roles."""

    def __init__(self):
        self._role_permissions: Dict[str, Set[str]] = {
            "admin": {"*"} | ALL_CAPABILITIES,
            "user": {"chat", "read_file", "search", "filesystem", "models", "memory", "knowledge"},
            "agent": {"tool_exec", "read_file", "write_file", "search", "browse", "filesystem", "browser", "models", "memory", "knowledge", "services", "workflows"},
        }
        self.audit = PermissionAudit()

    def grant_permission(self, role: str, permission: str) -> None:
        if role not in self._role_permissions:
            self._role_permissions[role] = set()
        self._role_permissions[role].add(permission)

    def check_permission(self, role: str, permission: str) -> bool:
        if role not in self._role_permissions:
            self.audit.record_check(role, permission, False)
            return False
        perms = self._role_permissions[role]
        granted = "*" in perms or permission in perms
        self.audit.record_check(role, permission, granted)
        return granted


class PermissionManager:
    """Master Capability-based Permission Manager overseeing approvals and profiles."""

    def __init__(self):
        self.engine = PermissionEngine()
        self.pending_approvals: Dict[str, ApprovalRequest] = {}
        self.sandbox_profiles: Dict[str, SandboxProfile] = {
            "strict": SandboxProfile(name="strict", allowed_capabilities={"memory", "knowledge"}, read_only_filesystem=True, network_access=False),
            "standard": SandboxProfile(name="standard", allowed_capabilities={"filesystem", "browser", "models", "memory", "knowledge", "services"}, read_only_filesystem=False, network_access=True),
        }

    def request_capability(self, agent_id: str, capability: str, reason: str = "") -> ApprovalRequest:
        import uuid
        req_id = str(uuid.uuid4())
        req = ApprovalRequest(request_id=req_id, agent_id=agent_id, capability=capability, reason=reason)
        self.pending_approvals[req_id] = req
        logger.info(f"Created capability ApprovalRequest '{req_id}' for agent '{agent_id}' ({capability})")
        return req

    def approve_request(self, request_id: str) -> bool:
        if request_id in self.pending_approvals:
            self.pending_approvals[request_id].status = "approved"
            return True
        return False

    def check(self, role: str, capability: str) -> bool:
        return self.engine.check_permission(role, capability)
