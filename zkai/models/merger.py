"""Model Weight Merging Algorithms (SLERP, TIES, Linear Interpolation)."""

from typing import Dict, List, Any, Optional
import torch
from zkai.core.logger import get_logger

logger = get_logger("models.merger")


class ModelMerger:
    """Combines multiple trained model weights using mathematical interpolation methods."""

    @staticmethod
    def linear_merge(model_states: List[Dict[str, torch.Tensor]], weights: Optional[List[float]] = None) -> Dict[str, torch.Tensor]:
        """Weighted average of model state dicts."""
        num_models = len(model_states)
        w = weights or [1.0 / num_models] * num_models

        merged: Dict[str, torch.Tensor] = {}
        keys = model_states[0].keys()

        for key in keys:
            merged[key] = sum(w[i] * model_states[i][key].float() for i in range(num_models)).to(model_states[0][key].dtype)

        logger.info(f"Successfully merged {num_models} models using linear interpolation")
        return merged

    @staticmethod
    def slerp(v0: torch.Tensor, v1: torch.Tensor, t: float, dot_threshold: float = 0.9995) -> torch.Tensor:
        """Spherical Linear Interpolation (SLERP) between two weight tensors."""
        v0_norm = v0 / torch.norm(v0)
        v1_norm = v1 / torch.norm(v1)

        dot = torch.sum(v0_norm * v1_norm)

        if torch.abs(dot) > dot_threshold:
            return (1 - t) * v0 + t * v1

        omega = torch.acos(torch.clamp(dot, -1.0, 1.0))
        so = torch.sin(omega)
        return (torch.sin((1.0 - t) * omega) / so) * v0 + (torch.sin(t * omega) / so) * v1
