"""MixedPrecisionTrainer handling Automatic Mixed Precision (AMP)."""

import torch
from zkai.core.logger import get_logger

logger = get_logger("training.precision")


class MixedPrecisionTrainer:
    """Manages FP16 / BF16 mixed precision training with gradient scaling."""

    def __init__(self, enabled: bool = True, dtype: torch.dtype = torch.float16):
        self.enabled = enabled
        self.dtype = dtype
        self.scaler = torch.cuda.amp.GradScaler(enabled=enabled)

    def autocast(self):
        return torch.cuda.amp.autocast(enabled=self.enabled, dtype=self.dtype)
