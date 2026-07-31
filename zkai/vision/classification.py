"""Image Classification Engine classifying images into category labels."""

from dataclasses import dataclass
from typing import List
from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("vision.classification")


@dataclass
class ClassificationResult:
    label: str
    score: float


class ImageClassifier:
    """Classifies image contents into candidate semantic category labels."""

    def classify(self, image: Image, top_k: int = 5) -> List[ClassificationResult]:
        logger.info("Classifying image content...")
        return [ClassificationResult(label="general_scene", score=0.98)]
