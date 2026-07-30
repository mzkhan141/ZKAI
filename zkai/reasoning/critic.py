"""ReasoningCritic for chain scoring."""

from zkai.evaluation.critic import Critic


class ReasoningCritic:
    """Scores quality and coherence of step-by-step reasoning chains."""

    def __init__(self):
        self.critic = Critic()

    def score_chain(self, chain_steps: list[str]) -> float:
        text = "\n".join(chain_steps)
        res = self.critic.evaluate(text)
        return res.score
