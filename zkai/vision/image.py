"""Image loading, preprocessing, transformation, and display container."""

from pathlib import Path
from typing import Any, Tuple, Union
import numpy as np
from PIL import Image as PILImage
from zkai.core.exceptions import VisionError
from zkai.core.logger import get_logger

logger = get_logger("vision.image")


class Image:
    """Unified Image container wrapping PIL and OpenCV data structures."""

    def __init__(self, data: Union[str, Path, PILImage.Image, np.ndarray]):
        if isinstance(data, (str, Path)):
            self._pil_image = PILImage.open(data).convert("RGB")
        elif isinstance(data, PILImage.Image):
            self._pil_image = data.convert("RGB")
        elif isinstance(data, np.ndarray):
            self._pil_image = PILImage.fromarray(data).convert("RGB")
        else:
            raise VisionError(f"Unsupported image input type: {type(data)}")

    @property
    def size(self) -> Tuple[int, int]:
        """Returns (width, height)."""
        return self._pil_image.size

    @property
    def width(self) -> int:
        return self._pil_image.width

    @property
    def height(self) -> int:
        return self._pil_image.height

    def to_numpy(self) -> np.ndarray:
        return np.array(self._pil_image)

    def to_pil(self) -> PILImage.Image:
        return self._pil_image

    def resize(self, width: int, height: int) -> "Image":
        resized = self._pil_image.resize((width, height), PILImage.Resampling.LANCZOS)
        return Image(resized)

    def save(self, file_path: str) -> None:
        self._pil_image.save(file_path)
        logger.info(f"Saved image to {file_path}")
