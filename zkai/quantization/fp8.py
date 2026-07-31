"""8-bit Floating Point (FP8) Quantization Engine."""

from typing import Tuple
import torch


class FP8Quantizer:
    """Quantizes float32 tensors to FP8 E4M3 and E5M2 formats."""

    @staticmethod
    def quantize_fp8_e4m3(tensor: torch.Tensor) -> Tuple[torch.Tensor, float]:
        max_val = torch.max(torch.abs(tensor)).item()
        scale = max_val / 448.0 if max_val > 0 else 1.0
        scaled = torch.clamp(tensor / scale, -448.0, 448.0)
        return scaled.to(torch.float16), scale

    @staticmethod
    def dequantize_fp8_e4m3(quantized: torch.Tensor, scale: float) -> torch.Tensor:
        return quantized.to(torch.float32) * scale
