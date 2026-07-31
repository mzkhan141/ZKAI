"""TrainingHooks for execution event listening."""

from typing import Callable, List


class TrainingHook:
    def __init__(self, fn: Callable):
        self.fn = fn

    def trigger(self, *args, **kwargs) -> None:
        self.fn(*args, **kwargs)
