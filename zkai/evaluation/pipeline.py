"""EvaluationPipeline connecting Critic, Verifier, Reflection, Scorer, and RetryManager."""

from typing import Callable
from zkai.evaluation.critic import Critic
from zkai.evaluation.verifier import Verifier
from zkai.evaluation.reflection import Reflection
from zkai.evaluation.scorer import Scorer
from zkai.evaluation.retry import RetryManager
from zkai.core.logger import get_logger

logger = get_logger("evaluation.pipeline")


class EvaluationPipeline:
    """Complete Self-Evaluation Pipeline orchestrator for ZKAI."""

    def __init__(self, confidence_threshold: float = 0.8, max_retries: int = 3):
        self.critic = Critic(quality_threshold=confidence_threshold)
        self.verifier = Verifier()
        self.reflection = Reflection()
        self.retry_manager = RetryManager(max_attempts=max_retries, threshold=confidence_threshold)

    def evaluate_and_refine(self, generator_fn: Callable[[str], str], prompt: str) -> str:
        """Executes generation through the self-evaluation pipeline."""
        return self.retry_manager.run_with_retry(generator_fn, prompt)
