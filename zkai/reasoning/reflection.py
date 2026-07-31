"""ReflectionEngine for structured self-reflection."""

from zkai.evaluation.reflection import Reflection


class ReflectionEngine:
    """Reflects on failed reasoning attempts to suggest corrective steps."""

    def __init__(self):
        self.reflection = Reflection()

    def reflect(self, task: str, error: str) -> str:
        res = self.reflection.reflect(task, error)
        return res.critique
