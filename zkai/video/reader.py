"""VideoReader for reading video streams."""

from pathlib import Path
from typing import Generator, Optional
from zkai.vision.image import Image

try:
    import cv2
except ImportError:
    cv2 = None


class VideoReader:
    """Frame-accurate video file reader."""

    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path) if cv2 else None

    @property
    def fps(self) -> float:
        if cv2 and self.cap:
            return self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        return 30.0

    @property
    def frame_count(self) -> int:
        if cv2 and self.cap:
            return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return 0

    def read_frames(self) -> Generator[Image, None, None]:
        if not cv2 or not self.cap:
            return
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield Image(rgb)
        self.cap.release()
