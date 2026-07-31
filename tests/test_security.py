"""Unit tests for Security subsystem."""

import pytest
from zkai.security import (
    AuditLog,
    CapabilityToken,
    EncryptedMemory,
    PermissionEngine,
    Policy,
    PolicyEngine,
    SecretsManager,
    TokenIssuer,
)


def test_secrets_manager():
    sm = SecretsManager(secret_key="test_key")
    sm.set_secret("API_KEY", "super_secret_val")
    assert sm.get_secret("API_KEY") == "super_secret_val"


def test_encrypted_memory():
    em = EncryptedMemory(key="test_key")
    em.store("user_pass", "secret123")
    assert em.retrieve("user_pass") == "secret123"


def test_permission_engine():
    pe = PermissionEngine()
    assert pe.check_permission("admin", "anything") is True
    assert pe.check_permission("user", "chat") is True
    assert pe.check_permission("user", "delete_db") is False


def test_token_issuer():
    tok = TokenIssuer.issue_token("agent_007", ["read_file", "write_file"])
    assert tok.is_valid() is True
    assert "read_file" in tok.capabilities
