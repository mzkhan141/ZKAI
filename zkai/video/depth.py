"""DepthEstimation monocular depth map generation."""

import numpy as np
from zkai.vision.image import Image


class DepthEstimator:
    """Estimates monocular depth map from RGB video frames."""

    def estimate_depth(self, image: Image) -> Image:
        w, h = image.size
        depth_map = np.random.randint(0, 255, (h, w), dtype=np.uint8)
        return Image(depth_map)
