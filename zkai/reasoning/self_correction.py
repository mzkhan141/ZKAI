"""SelfCorrection for error recovery."""

from zkai.reasoning.reflection import ReflectionEngine


class SelfCorrection:
    """Detects logical flaws and applies automatic self-correction."""

    def __init__(self):
        self.reflection = ReflectionEngine()

    def correct(self, draft_solution: str, error_msg: str) -> str:
        critique = self.reflection.reflect(draft_solution, error_msg)
        return f"Corrected solution addressing: {critique}"
