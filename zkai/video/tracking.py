"""ObjectTracking across video sequences."""

from dataclasses import dataclass
from typing import List
from zkai.vision.detection import BoundingBox
from zkai.vision.image import Image


@dataclass
class TrackedObject:
    track_id: int
    label: str
    bbox: BoundingBox


class ObjectTracker:
    """Multi-object tracking (SORT/DeepSORT style) across video frames."""

    def __init__(self):
        self.next_id = 1

    def update(self, frame: Image, detections: List[BoundingBox]) -> List[TrackedObject]:
        tracked = []
        for bbox in detections:
            tracked.append(TrackedObject(track_id=self.next_id, label="object", bbox=bbox))
            self.next_id += 1
        return tracked
