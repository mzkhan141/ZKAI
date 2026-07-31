"""VerifierAgent specialized in goal condition verification."""

from zkai.evaluation.verifier import Verifier


class VerifierAgent:
    """Specialized Agent for validating final goal conditions."""

    def __init__(self):
        self.verifier = Verifier()

    def verify(self, output: str) -> bool:
        res = self.verifier.verify(output)
        return res.is_valid
