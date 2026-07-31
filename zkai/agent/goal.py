"""Goal and SubTask management structures."""

from dataclasses import dataclass, field
import uuid
from typing import List, Optional


@dataclass
class SubTask:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    completed: bool = False
    result: Optional[str] = None


@dataclass
class Goal:
    title: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    subtasks: List[SubTask] = field(default_factory=list)
    completed: bool = False


class GoalManager:
    """Manages high-level agent goals and subtask decomposition."""

    def create_goal(self, title: str, description: str) -> Goal:
        return Goal(title=title, description=description)

    def add_subtask(self, goal: Goal, description: str) -> SubTask:
        sub = SubTask(description=description)
        goal.subtasks.append(sub)
        return sub
