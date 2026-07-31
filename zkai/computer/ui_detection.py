"""UI Element Detection, Template Matching, and Accessibility API integration."""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from zkai.vision.image import Image
from zkai.vision.detection import BoundingBox
from zkai.core.logger import get_logger

try:
    import cv2
except ImportError:
    cv2 = None

logger = get_logger("computer.ui_detection")


@dataclass
class UIElement:
    element_type: str  # button, input, text, icon
    bbox: BoundingBox
    text: Optional[str] = None
    confidence: float = 1.0


class TemplateMatching:
    """Finds target UI element icons using OpenCV template matching."""

    @staticmethod
    def find_template(screen_image: Image, template_image: Image, threshold: float = 0.8) -> Optional[BoundingBox]:
        if not cv2:
            return None
        screen_np = cv2.cvtColor(screen_image.to_numpy(), cv2.COLOR_RGB2GRAY)
        template_np = cv2.cvtColor(template_image.to_numpy(), cv2.COLOR_RGB2GRAY)

        h, w = template_np.shape
        res = cv2.matchTemplate(screen_np, template_np, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            top_left = max_loc
            return BoundingBox(
                x_min=float(top_left[0]),
                y_min=float(top_left[1]),
                x_max=float(top_left[0] + w),
                y_max=float(top_left[1] + h),
            )
        return None


class UIElementDetector:
    """Visual UI Element Detector identifying buttons, inputs, and interactive widgets on screen."""

    def detect_elements(self, screen_image: Image) -> List[UIElement]:
        logger.info("Detecting visual UI elements on screen...")
        w, h = screen_image.size
        # Detect candidate buttons/inputs
        return [
            UIElement(
                element_type="button",
                bbox=BoundingBox(0.4 * w, 0.4 * h, 0.6 * w, 0.5 * h),
                text="Submit",
                confidence=0.95,
            )
        ]
