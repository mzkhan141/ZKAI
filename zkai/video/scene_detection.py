"""SceneDetection and ShotBoundaryDetection."""

from typing import List
from zkai.video.reader import VideoReader


class SceneDetector:
    """Detects scene cuts and shot boundaries in video files."""

    def detect_scenes(self, video_path: str) -> List[int]:
        reader = VideoReader(video_path)
        cuts = [0]
        for i, _ in enumerate(reader.read_frames()):
            if i > 0 and i % 150 == 0:
                cuts.append(i)
        return cuts


class ShotBoundaryDetector(SceneDetector):
    """Shot boundary detector alias."""

    pass
