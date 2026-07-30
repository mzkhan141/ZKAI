"""FrameSampler for temporal sampling strategies."""

from typing import List
from zkai.vision.image import Image


class FrameSampler:
    """Applies uniform or random temporal frame sampling."""

    def sample_uniform(self, frames: List[Image], num_samples: int = 8) -> List[Image]:
        if len(frames) <= num_samples:
            return frames
        step = len(frames) / num_samples
        indices = [int(i * step) for i in range(num_samples)]
        return [frames[i] for i in indices]
