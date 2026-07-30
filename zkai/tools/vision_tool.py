"""VisionTool running OCR and object detection on images."""

from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult
from zkai.vision.image import Image
from zkai.vision.ocr import OCREngine


from zkai.core.logger import get_logger

logger = get_logger("tools.vision")


class VisionTool(Tool):
    """Tool running OCR and image analysis."""

    def __init__(self):
        meta = ToolMetadata(name="vision", description="Analyzes images and extracts text via OCR", category="vision")
        super().__init__(meta)
        self.ocr = OCREngine()

    def execute(self, image_path: str, **kwargs: Any) -> ToolResult:
        try:
            img = Image(image_path)
            text = self.ocr.read_text(img)
            return ToolResult(tool_name=self.metadata.name, success=True, result=text)
        except Exception as e:
            logger.error(f"VisionTool execution failed for '{image_path}': {e}")
            return ToolResult(tool_name=self.metadata.name, success=False, result="", error=str(e))
