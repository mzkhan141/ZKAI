"""Tests for AISession and SessionManager."""

import pytest
from zkai.session.session import AISession
from zkai.session.manager import SessionManager, SessionSerializer


def test_ai_session_serialization(tmp_path):
    session = AISession()
    session.conversation_history.append({"user": "Hello", "assistant": "Hi"})
    session.running_agents.append("coder_agent")
    session.desktop_layout = {"theme": "dark"}

    save_path = str(tmp_path / "test_session.json")
    SessionSerializer.save_to_file(session, save_path)

    restored = SessionSerializer.load_from_file(save_path)
    assert restored is not None
    assert restored.session_id == session.session_id
    assert restored.conversation_history[0]["user"] == "Hello"
    assert restored.running_agents == ["coder_agent"]


def test_session_manager(tmp_path):
    mgr = SessionManager(storage_dir=str(tmp_path / "snapshots"))
    session = mgr.create_session()

    session.knowledge_context.append("doc1.txt")
    mgr.save_session(session.session_id)

    retrieved = mgr.get_session(session.session_id)
    assert retrieved is not None
    assert "doc1.txt" in retrieved.knowledge_context

    mgr.terminate_session(session.session_id)
    assert len(mgr.list_active_sessions()) == 0
