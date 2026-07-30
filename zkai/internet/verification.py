"""FactVerifier, ConsensusDetector, and CrossReferencer for web facts."""

from dataclasses import dataclass
from typing import List, Dict, Any
from zkai.core.logger import get_logger

logger = get_logger("internet.verification")


@dataclass
class VerificationOutcome:
    statement: str
    verified: bool
    consensus_score: float
    supporting_sources: List[str]


class ConsensusDetector:
    """Detects claim consensus across multiple independent web sources."""

    def detect_consensus(self, statement: str, source_contents: List[str]) -> float:
        matches = sum(1 for text in source_contents if statement.lower() in text.lower())
        return min(1.0, matches / max(1, len(source_contents)))


class CrossReferencer:
    """Cross-references factual claims across retrieved web sources."""

    def cross_reference(self, statement: str, source_contents: List[str]) -> List[str]:
        return [text[:100] for text in source_contents if statement.lower() in text.lower()]


class FactVerifier:
    """Verifies statements against multi-source web evidence before answering."""

    def __init__(self):
        self.consensus_detector = ConsensusDetector()
        self.cross_referencer = CrossReferencer()

    def verify_fact(self, statement: str, source_contents: List[str]) -> VerificationOutcome:
        logger.info(f"Verifying fact statement across {len(source_contents)} web sources...")
        score = self.consensus_detector.detect_consensus(statement, source_contents)
        refs = self.cross_referencer.cross_reference(statement, source_contents)
        return VerificationOutcome(
            statement=statement,
            verified=(score >= 0.5),
            consensus_score=score,
            supporting_sources=refs,
        )
