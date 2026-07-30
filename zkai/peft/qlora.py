"""QLoRA (Quantized Low-Rank Adaptation) with 4-bit NormalFloat base weights."""

import torch
import torch.nn as nn
from zkai.models.lora import LoRAAdapter, LoRAConfig
from zkai.quantization.nf4 import NF4Quantizer


class QLoRAAdapter(LoRAAdapter):
    """QLoRA adapter layer freezing base linear weights in NF4 precision."""

    def __init__(self, linear_layer: nn.Linear, config: LoRAConfig):
        q_weight, scale = NF4Quantizer.quantize_nf4(linear_layer.weight.data)
        linear_layer.weight.data = NF4Quantizer.dequantize_nf4(q_weight, scale)
        super().__init__(linear_layer, config)
