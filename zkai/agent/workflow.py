"""Workflow and WorkflowStep structures."""

from dataclasses import dataclass
from typing import Callable, List, Any


@dataclass
class WorkflowStep:
    name: str
    action: Callable[[Any], Any]


class Workflow:
    """Executes ordered workflow steps."""

    def __init__(self):
        self.steps: List[WorkflowStep] = []

    def add_step(self, name: str, action: Callable[[Any], Any]) -> "Workflow":
        self.steps.append(WorkflowStep(name, action))
        return self

    def run(self, initial_input: Any) -> Any:
        current = initial_input
        for step in self.steps:
            current = step.action(current)
        return current
