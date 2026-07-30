"""Tests for AI Identity System."""

import pytest
from zkai.identity.identity import User, AgentIdentity, AuthenticationManager, AuthorizationManager
from zkai.identity.sync import IdentitySynchronizer, SessionBinder
from zkai.session.session import AISession


def test_identity_creation_and_auth():
    user = User("alice")
    user.capabilities.append("filesystem")

    auth_mgr = AuthenticationManager()
    token = auth_mgr.authenticate(user)
    assert token.subject == user.identity_id
    assert token.is_valid() is True


def test_identity_sync_and_session_binding():
    sync = IdentitySynchronizer()
    agent_id = AgentIdentity("researcher")
    sync.sync_identity(agent_id)

    fetched = sync.get_identity(agent_id.identity_id)
    assert fetched is not None
    assert fetched.name == "researcher"

    binder = SessionBinder()
    session = AISession()
    binder.bind(session, agent_id)
    assert binder.get_identity_id(session.session_id) == agent_id.identity_id
