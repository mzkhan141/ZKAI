"""Monitor, Screen Capture, and Screen Recording."""

from PIL import ImageGrab
from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("computer.monitor")


class ScreenCapture:
    """Captures desktop monitor screenshots."""

    def capture_screen(self) -> Image:
        """Captures active screen display as a ZKAI Image object."""
        logger.info("Capturing desktop screenshot...")
        pil_img = ImageGrab.grab()
        return Image(pil_img)


class Monitor:
    """Monitor interface wrapper."""

    def __init__(self):
        self.screen_capture = ScreenCapture()

    def screenshot(self) -> Image:
        return self.screen_capture.capture_screen()
