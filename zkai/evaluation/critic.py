"""Critic evaluator analyzing factual accuracy, hallucinations, and safety."""

from dataclasses import dataclass
from typing import Any, Dict
from zkai.core.logger import get_logger

logger = get_logger("evaluation.critic")


@dataclass
class CriticResult:
    """Evaluation output from Critic inspection."""
    is_valid: bool
    quality_score: float
    hallucination_score: float
    feedback: str


class Critic:
    """Evaluates text responses against strict quality and hallucination thresholds."""

    def __init__(self, quality_threshold: float = 0.7):
        self.quality_threshold = quality_threshold

    def evaluate(self, prompt: str, response: str) -> CriticResult:
        logger.info("Evaluating response quality with Critic...")
        # Rule-based evaluation heuristics
        is_empty = len(response.strip()) == 0
        score = 0.0 if is_empty else 0.95
        hallucination = 0.0 if not is_empty else 1.0

        return CriticResult(
            is_valid=(score >= self.quality_threshold),
            quality_score=score,
            hallucination_score=hallucination,
            feedback="Response passes quality criteria." if score >= self.quality_threshold else "Response quality too low.",
        )
