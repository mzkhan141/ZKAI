"""OpticalFlow estimation between adjacent frames."""

import numpy as np
from zkai.vision.image import Image

try:
    import cv2
except ImportError:
    cv2 = None


class OpticalFlowEstimator:
    """Computes dense optical flow fields between consecutive frames."""

    def compute_flow(self, prev_frame: Image, curr_frame: Image) -> np.ndarray:
        w, h = prev_frame.size
        if not cv2:
            return np.zeros((h, w, 2), dtype=np.float32)
        p_gray = cv2.cvtColor(np.array(prev_frame.raw), cv2.COLOR_RGB2GRAY)
        c_gray = cv2.cvtColor(np.array(curr_frame.raw), cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(p_gray, c_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        return flow
