"""Reflection evaluator summarizing mistakes and generating corrective prompts."""

from dataclasses import dataclass
from zkai.core.logger import get_logger

logger = get_logger("evaluation.reflection")


@dataclass
class ReflectionResult:
    """Summary of self-reflection analysis."""
    insights: str
    suggested_revision: str


class Reflection:
    """Reflects on failed verification or low critic scores to revise outputs."""

    def reflect(self, query: str, attempt: str, feedback: str) -> ReflectionResult:
        logger.info("Performing self-reflection on failed attempt...")
        return ReflectionResult(
            insights=f"Attempt failed due to: {feedback}",
            suggested_revision=f"Re-run generation for '{query}' addressing feedback: {feedback}",
        )
