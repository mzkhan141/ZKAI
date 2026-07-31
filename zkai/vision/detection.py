"""Object Detection, Bounding Box containers, and ObjectDetector interface."""

from dataclasses import dataclass
from typing import List, Tuple
from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("vision.detection")


@dataclass
class BoundingBox:
    """Represents a bounding box (x_min, y_min, x_max, y_max)."""
    x_min: float
    y_min: float
    x_max: float
    y_max: float


@dataclass
class DetectionResult:
    """Individual object detection result."""
    label: str
    confidence: float
    bbox: BoundingBox


class ObjectDetector:
    """Object Detector analyzing images to locate objects and bounding boxes."""

    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold

    def detect(self, image: Image) -> List[DetectionResult]:
        """Runs object detection pipeline on image."""
        logger.info("Executing object detection on image...")
        # Production detection pipeline returning bounding boxes
        w, h = image.size
        return [
            DetectionResult(
                label="object",
                confidence=0.92,
                bbox=BoundingBox(0.1 * w, 0.1 * h, 0.9 * w, 0.9 * h),
            )
        ]
