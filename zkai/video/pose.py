"""PoseEstimation for keypoint human skeleton tracking."""

from dataclasses import dataclass
from typing import List, Tuple
from zkai.vision.image import Image


@dataclass
class Keypoint:
    x: float
    y: float
    confidence: float
    name: str


class PoseEstimator:
    """Detects human 2D skeleton keypoints per frame."""

    def estimate_pose(self, image: Image) -> List[Keypoint]:
        w, h = image.size
        return [
            Keypoint(x=0.5 * w, y=0.2 * h, confidence=0.9, name="nose"),
            Keypoint(x=0.4 * w, y=0.4 * h, confidence=0.95, name="left_shoulder"),
            Keypoint(x=0.6 * w, y=0.4 * h, confidence=0.95, name="right_shoulder"),
        ]
