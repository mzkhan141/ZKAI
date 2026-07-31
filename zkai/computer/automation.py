"""ActionSequence and high-level Computer Automation controller."""

from dataclasses import dataclass
from typing import List, Union
from zkai.computer.mouse import Mouse
from zkai.computer.keyboard import Keyboard
from zkai.computer.monitor import ScreenCapture
from zkai.core.logger import get_logger

logger = get_logger("computer.automation")


@dataclass
class Action:
    action_type: str  # click, move, type, hotkey, wait
    target: Union[tuple[int, int], str, float]


class ActionSequence:
    """Sequence of executable computer GUI actions."""

    def __init__(self):
        self.actions: List[Action] = []

    def add_click(self, x: int, y: int) -> "ActionSequence":
        self.actions.append(Action("click", (x, y)))
        return self

    def add_type(self, text: str) -> "ActionSequence":
        self.actions.append(Action("type", text))
        return self


class Automation:
    """Executes computer GUI action sequences using visual feedback."""

    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.screen_capture = ScreenCapture()

    def execute_sequence(self, sequence: ActionSequence) -> None:
        logger.info(f"Executing automation sequence with {len(sequence.actions)} actions...")
        for act in sequence.actions:
            if act.action_type == "click" and isinstance(act.target, tuple):
                self.mouse.click(act.target[0], act.target[1])
            elif act.action_type == "type" and isinstance(act.target, str):
                self.keyboard.type_text(act.target)
