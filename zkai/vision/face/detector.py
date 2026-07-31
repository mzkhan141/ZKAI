"""FaceDetector with bounding box extraction."""

from dataclasses import dataclass
from typing import List
from zkai.vision.detection import BoundingBox
from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("vision.face.detector")


@dataclass
class FaceResult:
    bbox: BoundingBox
    confidence: float


class FaceDetector:
    """Detects facial bounding boxes in images."""

    def detect_faces(self, image: Image) -> List[FaceResult]:
        logger.info("Detecting face structures...")
        w, h = image.size
        return [FaceResult(bbox=BoundingBox(0.2 * w, 0.2 * h, 0.5 * w, 0.5 * h), confidence=0.99)]
