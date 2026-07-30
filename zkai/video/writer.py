"""VideoWriter for writing video output streams."""

from pathlib import Path
import numpy as np
from zkai.vision.image import Image

try:
    import cv2
except ImportError:
    cv2 = None


class VideoWriter:
    """Encodes frame streams to video container files."""

    def __init__(self, output_path: str, fps: float = 30.0, resolution: tuple[int, int] = (640, 480)):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        if cv2:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)
        else:
            self.writer = None

    def write_frame(self, image: Image) -> None:
        if cv2 and self.writer:
            bgr = cv2.cvtColor(np.array(image.raw), cv2.COLOR_RGB2BGR)
            self.writer.write(bgr)

    def release(self) -> None:
        if cv2 and self.writer:
            self.writer.release()
