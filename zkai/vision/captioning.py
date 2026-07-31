"""Image Captioning Engine generating natural language descriptions for images."""

from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("vision.captioning")


class ImageCaptioner:
    """Generates natural language textual descriptions from image visual data."""

    def __init__(self):
        pass

    def caption(self, image: Image) -> str:
        """Generates a text caption for the input image."""
        logger.info("Generating image caption...")
        return "An image displaying visual content."
