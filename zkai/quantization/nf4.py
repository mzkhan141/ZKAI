"""NormalFloat4 (NF4) Quantization Engine for QLoRA."""

from typing import Tuple
import torch

NF4_MAP = torch.tensor([
    -1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453,
    -0.28444117307662964, -0.18477343022823334, -0.09105003625154495, 0.0,
    0.07958029955625534, 0.16093020141124725, 0.24611230194568634, 0.33791807293891907,
    0.44070982933044434, 0.5626170039176941, 0.7229568362236023, 1.0
])


class NF4Quantizer:
    """Quantizes float weights using NormalFloat4 distribution optimized for neural network weights."""

    @staticmethod
    def quantize_nf4(tensor: torch.Tensor) -> Tuple[torch.Tensor, float]:
        abs_max = torch.max(torch.abs(tensor)).item()
        scale = abs_max if abs_max > 0 else 1.0
        normalized = tensor / scale
        nf4_device = NF4_MAP.to(tensor.device)
        diff = torch.abs(normalized.unsqueeze(-1) - nf4_device)
        indices = torch.argmin(diff, dim=-1).to(torch.uint8)
        return indices, scale

    @staticmethod
    def dequantize_nf4(indices: torch.Tensor, scale: float) -> torch.Tensor:
        nf4_device = NF4_MAP.to(indices.device)
        quantized_vals = nf4_device[indices.to(torch.long)]
        return quantized_vals * scale
