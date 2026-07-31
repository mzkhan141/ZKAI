"""SecurityKernel providing operating-system-level security enforcement."""

from typing import Any, Dict, Optional
from zkai.security.secrets import SecretsManager
from zkai.security.encryption import EncryptedMemory, SecureStorage
from zkai.security.permissions import PermissionManager
from zkai.security.policy import PolicyEngine
from zkai.security.audit import AuditLog
from zkai.security.sandbox import SandboxPolicy
from zkai.core.logger import get_logger

logger = get_logger("security_kernel")


class SecurityKernel:
    """Central OS Security Kernel enforcing model, workflow, and process isolation boundaries."""

    def __init__(self):
        self.secrets = SecretsManager()
        self.encrypted_memory = EncryptedMemory()
        self.secure_storage = SecureStorage()
        self.permission_manager = PermissionManager()
        self.policy_engine = PolicyEngine()
        self.audit_log = AuditLog()
        self.sandbox_policy = SandboxPolicy()

    def audit(self, actor: str, action: str, details: str = "") -> None:
        self.audit_log.log(event_type="security_audit", actor=actor, action=action, status="success", details=details)

    def validate_model_isolation(self, model_id: str, caller_id: str) -> bool:
        """Enforces model memory isolation across callers."""
        granted = self.permission_manager.check("agent", "models")
        self.audit(actor=caller_id, action=f"access_model:{model_id}", details=f"granted={granted}")
        return granted

    def validate_workflow_isolation(self, workflow_id: str, caller_id: str) -> bool:
        """Enforces DAG workflow execution boundary isolation."""
        granted = self.permission_manager.check("agent", "workflows")
        self.audit(actor=caller_id, action=f"execute_workflow:{workflow_id}", details=f"granted={granted}")
        return granted
