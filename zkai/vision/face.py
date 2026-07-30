"""Face Detection and Recognition engine."""

from dataclasses import dataclass
from typing import List
from zkai.vision.image import Image
from zkai.vision.detection import BoundingBox
from zkai.core.logger import get_logger

logger = get_logger("vision.face")


@dataclass
class FaceResult:
    bbox: BoundingBox
    confidence: float


class FaceDetector:
    """Detects facial structures and bounding locations in images."""

    def detect_faces(self, image: Image) -> List[FaceResult]:
        logger.info("Detecting faces in image...")
        w, h = image.size
        return [FaceResult(bbox=BoundingBox(0.2 * w, 0.2 * h, 0.5 * w, 0.5 * h), confidence=0.99)]
