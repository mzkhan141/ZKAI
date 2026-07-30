"""VisionAgent specialized in visual inspection and OCR."""

from zkai.vision.ocr import OCREngine
from zkai.vision.image import Image


class VisionAgent:
    """Specialized Agent for image perception, OCR, and scene analysis."""

    def __init__(self):
        self.ocr = OCREngine()

    def inspect_image(self, image_path: str) -> str:
        img = Image(image_path)
        return self.ocr.read_text(img)
