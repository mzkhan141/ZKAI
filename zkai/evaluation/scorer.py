"""Scorer aggregating overall confidence and composite quality metrics."""

from dataclasses import dataclass
from zkai.evaluation.critic import CriticResult
from zkai.evaluation.verifier import VerificationResult


@dataclass
class ConfidenceScore:
    """Overall confidence metric representation."""
    composite_score: float
    confidence_level: str  # HIGH, MEDIUM, LOW


class Scorer:
    """Combines critic, verifier, and metric scores into a unified confidence index."""

    @staticmethod
    def calculate_confidence(critic_res: CriticResult, verifier_res: VerificationResult) -> ConfidenceScore:
        base_score = critic_res.quality_score
        penalty = 0.3 if not verifier_res.passed else 0.0

        final_score = max(0.0, base_score - penalty)

        if final_score >= 0.8:
            level = "HIGH"
        elif final_score >= 0.5:
            level = "MEDIUM"
        else:
            level = "LOW"

        return ConfidenceScore(composite_score=final_score, confidence_level=level)
