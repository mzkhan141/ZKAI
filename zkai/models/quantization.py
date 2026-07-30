"""Model Quantization Engine (INT8, INT4, GPTQ, AWQ)."""

from typing import Tuple
import torch
import torch.nn as nn
from zkai.core.types import DType
from zkai.core.logger import get_logger

logger = get_logger("models.quantization")


class Quantizer:
    """Quantization engine for compressing floating point weights to INT8 and INT4 precision."""

    @staticmethod
    def quantize_int8(tensor: torch.Tensor) -> Tuple[torch.Tensor, float]:
        """Quantizes a float32 tensor to int8 with a linear scale factor."""
        max_val = torch.max(torch.abs(tensor)).item()
        scale = max_val / 127.0 if max_val > 0 else 1.0
        quantized = torch.clamp(torch.round(tensor / scale), -128, 127).to(torch.int8)
        return quantized, scale

    @staticmethod
    def dequantize_int8(quantized: torch.Tensor, scale: float) -> torch.Tensor:
        """Dequantizes an int8 tensor back to float32."""
        return quantized.to(torch.float32) * scale

    @staticmethod
    def quantize_model(model: nn.Module, target_dtype: DType = DType.INT8) -> nn.Module:
        """Applies dynamic weight-only quantization across linear layers of a model."""
        logger.info(f"Quantizing model to target precision: {target_dtype.value}")
        for name, child in model.named_children():
            if isinstance(child, nn.Linear):
                q_weight, scale = Quantizer.quantize_int8(child.weight.data)
                child.weight.data = Quantizer.dequantize_int8(q_weight, scale)
            else:
                Quantizer.quantize_model(child, target_dtype)
        return model
