"""FrameExtractor for sampling keyframes from video files."""

from typing import List
from zkai.video.reader import VideoReader
from zkai.vision.image import Image


class FrameExtractor:
    """Extracts keyframes or uniformly sampled frames from video."""

    def extract_keyframes(self, video_path: str, stride: int = 30) -> List[Image]:
        reader = VideoReader(video_path)
        frames = []
        for i, frame in enumerate(reader.read_frames()):
            if i % stride == 0:
                frames.append(frame)
        return frames
