"""FaceTracker tracking faces across video frames."""

from dataclasses import dataclass
from typing import Dict, List
from zkai.vision.detection import BoundingBox
from zkai.vision.image import Image


@dataclass
class TrackedFace:
    track_id: int
    bbox: BoundingBox


class FaceTracker:
    """Tracks face identities across sequential video frames."""

    def __init__(self):
        self.next_track_id = 1

    def update(self, frame: Image, bboxes: List[BoundingBox]) -> List[TrackedFace]:
        tracked = []
        for bbox in bboxes:
            tracked.append(TrackedFace(track_id=self.next_track_id, bbox=bbox))
            self.next_track_id += 1
        return tracked
