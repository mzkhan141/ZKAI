"""Tests for SecurityKernel and PermissionManager."""

import pytest
from zkai.security_kernel.kernel import SecurityKernel
from zkai.security.permissions import PermissionManager, ALL_CAPABILITIES


def test_permission_manager_capabilities():
    pm = PermissionManager()
    assert pm.check("admin", "filesystem") is True
    assert pm.check("admin", "network") is True
    assert pm.check("user", "filesystem") is True

    req = pm.request_capability("agent_1", "terminal", reason="Run build command")
    assert req.status == "pending"
    approved = pm.approve_request(req.request_id)
    assert approved is True
    assert req.status == "approved"


def test_security_kernel_isolation():
    sk = SecurityKernel()
    assert sk.validate_model_isolation("model_v1", "caller_agent") is True
    assert sk.validate_workflow_isolation("flow_123", "caller_agent") is True
    assert len(sk.audit_log.entries) >= 2
