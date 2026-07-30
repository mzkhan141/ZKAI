"""Plan, Action, and ExecutionGraph abstractions."""

from dataclasses import dataclass, field
import uuid
from typing import List, Dict, Any, Optional


@dataclass
class Action:
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Plan:
    goal_id: str
    actions: List[Action] = field(default_factory=list)


class ExecutionGraph:
    """DAG graph of dependent planned actions."""

    def __init__(self):
        self.nodes: Dict[str, Action] = {}
        self.edges: Dict[str, List[str]] = {}

    def add_action(self, action: Action, depends_on: Optional[List[str]] = None) -> None:
        self.nodes[action.action_id] = action
        self.edges[action.action_id] = depends_on or []
