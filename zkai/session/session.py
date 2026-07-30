"""AISession preserving conversation, memory, workflow, agent, and workspace states."""

import uuid
from typing import Any, Dict, List, Optional
from zkai.storage.session_store import SessionStore
from zkai.core.logger import get_logger

logger = get_logger("session")


class AISession:
    """Persistent operating session capturing complete OS state for restoration."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id: str = session_id or str(uuid.uuid4())
        self.conversation_history: List[Dict[str, Any]] = []
        self.running_workflows: List[str] = []
        self.running_agents: List[str] = []
        self.browser_state: Dict[str, Any] = {}
        self.desktop_layout: Dict[str, Any] = {}
        self.model_state: Dict[str, Any] = {}
        self.knowledge_context: List[str] = []
        self.workspace_state: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "running_workflows": self.running_workflows,
            "running_agents": self.running_agents,
            "browser_state": self.browser_state,
            "desktop_layout": self.desktop_layout,
            "model_state": self.model_state,
            "knowledge_context": self.knowledge_context,
            "workspace_state": self.workspace_state,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AISession":
        session = cls(session_id=data.get("session_id"))
        session.conversation_history = data.get("conversation_history", [])
        session.running_workflows = data.get("running_workflows", [])
        session.running_agents = data.get("running_agents", [])
        session.browser_state = data.get("browser_state", {})
        session.desktop_layout = data.get("desktop_layout", {})
        session.model_state = data.get("model_state", {})
        session.knowledge_context = data.get("knowledge_context", [])
        session.workspace_state = data.get("workspace_state", {})
        return session
