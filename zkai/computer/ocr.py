"""ComputerOCR for extracting text and bounding boxes directly from screen captures."""

from typing import List, Dict, Any
from zkai.vision.ocr import OCREngine
from zkai.computer.monitor import ScreenCapture
from zkai.core.logger import get_logger

logger = get_logger("computer.ocr")


class ComputerOCR:
    """Optical Character Recognition dedicated to active screen text extraction."""

    def __init__(self):
        self.ocr_engine = OCREngine()
        self.screen_capture = ScreenCapture()

    def read_screen_text(self) -> str:
        """Takes a screenshot and extracts all visible screen text."""
        screen_image = self.screen_capture.capture_screen()
        return self.ocr_engine.read_text(screen_image)

    def find_text_location(self, target_text: str) -> List[Dict[str, Any]]:
        """Finds bounding box coordinates of specific text visible on screen."""
        screen_image = self.screen_capture.capture_screen()
        details = self.ocr_engine.read_details(screen_image)
        return [d for d in details if target_text.lower() in d["text"].lower()]
