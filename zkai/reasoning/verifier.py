"""ReasoningVerifier for step verification."""

from zkai.evaluation.verifier import Verifier


class ReasoningVerifier:
    """Verifies validity of each individual step in a reasoning chain."""

    def __init__(self):
        self.verifier = Verifier()

    def verify_step(self, step: str) -> bool:
        res = self.verifier.verify(step)
        return res.is_valid
