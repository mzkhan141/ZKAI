"""Camera hardware interface for live webcam capture."""

from zkai.vision.image import Image
from zkai.core.exceptions import VisionError
from zkai.core.logger import get_logger

try:
    import cv2
except ImportError:
    cv2 = None

logger = get_logger("vision.camera")


class Camera:
    """Live camera video capture device interface."""

    def __init__(self, camera_id: int = 0, device_index: int = 0):
        self.device_index = device_index or camera_id
        self.cap = cv2.VideoCapture(self.device_index) if cv2 else None

    def read(self) -> Image:
        return self.capture()

    def capture(self) -> Image:
        """Captures a single frame from the camera."""
        if not cv2 or not self.cap:
            raise VisionError("OpenCV (cv2) not available.")

        if not self.cap.isOpened():
            self.cap.open(self.device_index)

        ret, frame = self.cap.read()
        if not ret or frame is None:
            raise VisionError(f"Failed to capture frame from camera device index {self.device_index}")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image(frame_rgb)

    def release(self) -> None:
        if cv2 and self.cap and self.cap.isOpened():
            self.cap.release()
