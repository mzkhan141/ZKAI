"""SessionManager, SessionSerializer, and AutoSaveManager for session persistence."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from zkai.session.session import AISession
from zkai.storage.session_store import SessionStore
from zkai.core.logger import get_logger

logger = get_logger("session.manager")


class SessionSerializer:
    """Serializes and deserializes AISession instances to JSON files."""

    @staticmethod
    def save_to_file(session: AISession, filepath: str) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, indent=2)
        logger.info(f"Saved AISession '{session.session_id}' to {filepath}")

    @staticmethod
    def load_from_file(filepath: str) -> Optional[AISession]:
        path = Path(filepath)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AISession.from_dict(data)


class AutoSaveManager:
    """Background periodic session snapshot save manager."""

    def __init__(self, session_manager: "SessionManager", storage_dir: str = "./session_snapshots"):
        self.session_manager = session_manager
        self.storage_dir = Path(storage_dir)

    def auto_save_all(self) -> int:
        count = 0
        for session in self.session_manager.list_active_sessions():
            filepath = self.storage_dir / f"session_{session.session_id}.json"
            SessionSerializer.save_to_file(session, str(filepath))
            count += 1
        return count


class SessionManager:
    """Master Session Manager creating, restoring, listing, and persisting AI sessions."""

    def __init__(self, storage_dir: str = "./session_snapshots"):
        self.storage_dir = storage_dir
        self.store = SessionStore()
        self.active_sessions: Dict[str, AISession] = {}
        self.auto_save = AutoSaveManager(self, storage_dir=storage_dir)

    def create_session(self) -> AISession:
        session = AISession()
        self.active_sessions[session.session_id] = session
        self.store.create_session(session.to_dict())
        logger.info(f"Created new AISession '{session.session_id}'")
        return session

    def get_session(self, session_id: str) -> Optional[AISession]:
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        filepath = Path(self.storage_dir) / f"session_{session_id}.json"
        restored = SessionSerializer.load_from_file(str(filepath))
        if restored:
            self.active_sessions[restored.session_id] = restored
        return restored

    def save_session(self, session_id: str) -> bool:
        session = self.get_session(session_id)
        if not session:
            return False
        filepath = Path(self.storage_dir) / f"session_{session.session_id}.json"
        SessionSerializer.save_to_file(session, str(filepath))
        return True

    def list_active_sessions(self) -> List[AISession]:
        return list(self.active_sessions.values())

    def terminate_session(self, session_id: str) -> None:
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        self.store.terminate_session(session_id)
