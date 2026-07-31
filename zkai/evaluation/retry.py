"""RetryManager orchestrating self-correction loops for low-confidence results."""

from typing import Callable, Optional, Any
from zkai.evaluation.critic import Critic
from zkai.evaluation.verifier import Verifier
from zkai.evaluation.scorer import Scorer
from zkai.core.logger import get_logger

logger = get_logger("evaluation.retry")


class RetryManager:
    """Manages iterative retry and refinement loops until threshold confidence is reached."""

    def __init__(self, max_attempts: int = 3, threshold: float = 0.8):
        self.max_attempts = max_attempts
        self.threshold = threshold
        self.critic = Critic()
        self.verifier = Verifier()

    def run_with_retry(self, generator_fn: Callable[[str], str], prompt: str) -> str:
        current_prompt = prompt
        attempts = 0

        while attempts < self.max_attempts:
            attempts += 1
            logger.info(f"Self-Evaluation attempt {attempts}/{self.max_attempts}...")
            response = generator_fn(current_prompt)

            c_res = self.critic.evaluate(prompt, response)
            v_res = self.verifier.verify(response)
            score = Scorer.calculate_confidence(c_res, v_res)

            if score.composite_score >= self.threshold:
                logger.info(f"Attempt {attempts} passed confidence threshold ({score.composite_score:.2f})")
                return response

            logger.warning(f"Attempt {attempts} below confidence threshold ({score.composite_score:.2f}). Refining prompt...")
            current_prompt = f"{prompt}\n[Correction: Improve output quality and satisfy constraints]."

        return response
