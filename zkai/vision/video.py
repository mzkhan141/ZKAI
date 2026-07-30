"""Video frame extraction and video stream processor."""

from pathlib import Path
from typing import Generator, List
from zkai.vision.image import Image
from zkai.core.logger import get_logger

try:
    import cv2
except ImportError:
    cv2 = None

logger = get_logger("vision.video")


class Video:
    """Video container for decoding video files and iterating over frames."""

    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path) if cv2 else None

    def extract_frames(self, sample_rate: int = 1) -> Generator[Image, None, None]:
        if not cv2 or not self.cap:
            return
        frame_idx = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            if frame_idx % sample_rate == 0:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                yield Image(frame_rgb)
            frame_idx += 1
        self.cap.release()
