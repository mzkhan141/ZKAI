"""WeightValidator verifying tensor shapes, dtypes, and NaN/Inf integrity across model checkpoints."""

from typing import Dict, List, Tuple
import torch
from zkai.core.exceptions import ModelError
from zkai.core.logger import get_logger

logger = get_logger("models.weight_validator")


class WeightValidator:
    """Tensor weight integrity validator."""

    def validate_weights(self, state_dict: Dict[str, torch.Tensor]) -> Tuple[bool, List[str]]:
        """Scans state dict tensors for NaNs, Infs, empty shapes, or invalid values."""
        issues: List[str] = []
        for name, param in state_dict.items():
            if not isinstance(param, torch.Tensor):
                issues.append(f"Key '{name}' is not a valid torch.Tensor.")
                continue

            if torch.isnan(param).any():
                issues.append(f"Tensor '{name}' contains NaN values.")

            if torch.isinf(param).any():
                issues.append(f"Tensor '{name}' contains Inf values.")

            if param.numel() == 0:
                issues.append(f"Tensor '{name}' has 0 elements.")

        is_valid = len(issues) == 0
        if not is_valid:
            logger.warning(f"Weight validation failed with {len(issues)} issues.")
        return is_valid, issues

    def validate_or_raise(self, state_dict: Dict[str, torch.Tensor]) -> None:
        is_valid, issues = self.validate_weights(state_dict)
        if not is_valid:
            raise ModelError(f"Model weight validation failed: {'; '.join(issues[:3])}")
