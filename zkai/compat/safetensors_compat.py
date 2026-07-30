"""SafetensorsCompat wrapper for loading and saving safetensors files."""

from typing import Any, Dict, Optional
import torch
from zkai.core.logger import get_logger

logger = get_logger("compat.safetensors")

try:
    from safetensors.torch import load_file, save_file
except ImportError:
    load_file = None
    save_file = None


class SafetensorsCompat:
    """Safetensors binary container file interface."""

    def load(self, filepath: str) -> Dict[str, torch.Tensor]:
        if load_file:
            return load_file(filepath)
        logger.warning("safetensors library not installed; torch fallback used.")
        return torch.load(filepath, map_location="cpu")

    def save(self, state_dict: Dict[str, torch.Tensor], filepath: str) -> None:
        if save_file:
            save_file(state_dict, filepath)
        else:
            torch.save(state_dict, filepath)
