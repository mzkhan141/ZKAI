"""4-bit Integer (INT4) Quantization Engine."""

from typing import Tuple
import torch
import torch.nn as nn
from zkai.quantization.base import QuantizationConfig


class INT4Quantizer:
    """Quantizes float32 tensors to 4-bit integer representation with scale/zero-point."""

    @staticmethod
    def quantize_int4(tensor: torch.Tensor, group_size: int = 128) -> Tuple[torch.Tensor, torch.Tensor]:
        """Quantizes float32 tensor to grouped int8 container holding int4 values [-8, 7]."""
        shape = tensor.shape
        tensor_flat = tensor.reshape(-1, group_size) if tensor.numel() % group_size == 0 else tensor.reshape(1, -1)
        max_val = torch.max(torch.abs(tensor_flat), dim=-1, keepdim=True).values
        scale = max_val / 7.0
        scale = torch.where(scale == 0, torch.ones_like(scale), scale)

        quantized = torch.clamp(torch.round(tensor_flat / scale), -8, 7).to(torch.int8)
        return quantized.reshape(shape), scale.reshape(-1)

    @staticmethod
    def dequantize_int4(quantized: torch.Tensor, scale: torch.Tensor, group_size: int = 128) -> torch.Tensor:
        """Dequantizes int4 stored in int8 container back to float32."""
        shape = quantized.shape
        q_flat = quantized.reshape(-1, group_size) if quantized.numel() % group_size == 0 else quantized.reshape(1, -1)
        scale_flat = scale.reshape(-1, 1)
        dequantized = q_flat.to(torch.float32) * scale_flat
        return dequantized.reshape(shape)
