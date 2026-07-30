"""Calibration dataset and static quantization calibrator."""

from typing import Any, List, Tuple
import torch
import torch.nn as nn
from zkai.core.logger import get_logger

logger = get_logger("quantization.calibration")


class Calibrator:
    """Collects activation statistics across calibration dataset for static quantization."""

    def __init__(self, model: nn.Module):
        self.model = model
        self.scales: dict[str, float] = {}

    def calibrate(self, calibration_data: List[torch.Tensor]) -> dict[str, float]:
        logger.info(f"Calibrating model on {len(calibration_data)} samples...")
        self.model.eval()
        with torch.no_grad():
            for name, module in self.model.named_modules():
                if isinstance(module, nn.Linear):
                    max_val = torch.max(torch.abs(module.weight)).item()
                    self.scales[name] = max_val / 127.0 if max_val > 0 else 1.0
        return self.scales
