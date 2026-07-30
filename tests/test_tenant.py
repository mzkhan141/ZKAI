"""Unit tests for Multi-Tenant OS, Workspace Isolation, and Tenant Security."""

import pytest
from zkai.identity import (
    TenantManager,
    WorkspaceIsolation,
)


def test_tenant_manager_creation():
    manager = TenantManager()
    tenant = manager.create_tenant("Acme Corp", tier="enterprise")
    assert tenant.name == "Acme Corp"
    assert tenant.tier == "enterprise"
    assert tenant.tenant_id in manager.security.keys


def test_workspace_isolation():
    isolation = WorkspaceIsolation()
    isolation.bind("ws_100", "tenant_a")
    
    assert isolation.validate_access("tenant_a", "ws_100")
    assert not isolation.validate_access("tenant_b", "ws_100")
