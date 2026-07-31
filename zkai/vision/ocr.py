"""Optical Character Recognition (OCR) Engine wrapping EasyOCR with fallback."""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from zkai.vision.image import Image
from zkai.core.logger import get_logger

try:
    import easyocr
except ImportError:
    easyocr = None

logger = get_logger("vision.ocr")


class OCREngine:
    """EasyOCR wrapper for extracting text and bounding boxes from image inputs."""

    def __init__(self, languages: Optional[List[str]] = None, gpu: bool = True):
        langs = languages or ["en"]
        self.reader = easyocr.Reader(langs, gpu=gpu) if easyocr else None

    def read_text(self, image: Image) -> str:
        """Extracts plain raw text string from an image."""
        if not easyocr or not self.reader:
            return ""
        img_np = image.to_numpy()
        results = self.reader.readtext(img_np, detail=0)
        return " ".join(results)

    def read_details(self, image: Image) -> List[Dict[str, Any]]:
        """Extracts detailed OCR bounding boxes, text, and confidence scores."""
        if not easyocr or not self.reader:
            return []
        img_np = image.to_numpy()
        raw_results = self.reader.readtext(img_np)
        output = []
        for bbox, text, prob in raw_results:
            output.append({
                "bbox": bbox,
                "text": text,
                "confidence": float(prob),
            })
        return output
