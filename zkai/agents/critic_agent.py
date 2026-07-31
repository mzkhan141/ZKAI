"""CriticAgent specialized in execution outcome critique."""

from zkai.evaluation.critic import Critic


class CriticAgent:
    """Specialized Agent for reviewing outputs and detecting errors."""

    def __init__(self):
        self.critic = Critic()

    def evaluate(self, result_text: str) -> bool:
        res = self.critic.evaluate(result_text)
        return res.passed
