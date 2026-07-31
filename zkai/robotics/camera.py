"""RobotCamera device abstraction extending vision Camera."""

from typing import Optional
from zkai.vision.camera import Camera
from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("robotics.camera")


class RobotCamera(Camera):
    """Camera device wrapper specifically for robot vision sensors."""

    def __init__(self, camera_id: int = 0, fps: int = 30):
        super().__init__(camera_id=camera_id)
        self.fps = fps

    def capture_frame(self) -> Optional[Image]:
        return self.read()
