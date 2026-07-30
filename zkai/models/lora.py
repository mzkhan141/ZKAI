"""Low-Rank Adaptation (LoRA) and QLoRA fine-tuning primitives."""

import math
from dataclasses import dataclass, field
from typing import List, Optional
import torch
import torch.nn as nn
from zkai.core.logger import get_logger

logger = get_logger("models.lora")


@dataclass
class LoRAConfig:
    """Configuration settings for LoRA fine-tuning adapters."""
    r: int = 8
    lora_alpha: float = 16.0
    lora_dropout: float = 0.05
    target_modules: List[str] = field(default_factory=lambda: ["q_proj", "v_proj"])


class LoRAAdapter(nn.Module):
    """LoRA Low-Rank decomposition linear adapter layer."""

    def __init__(self, linear_layer: nn.Linear, config: LoRAConfig):
        super().__init__()
        self.r = config.r
        self.lora_alpha = config.lora_alpha
        self.scaling = self.lora_alpha / self.r

        in_features = linear_layer.in_features
        out_features = linear_layer.out_features

        self.linear = linear_layer
        self.lora_A = nn.Parameter(torch.zeros((self.r, in_features)))
        self.lora_B = nn.Parameter(torch.zeros((out_features, self.r)))
        self.dropout = nn.Dropout(config.lora_dropout)

        # Initialize weights
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        nn.init.zeros_(self.lora_B)

        # Freeze original linear weights
        self.linear.weight.requires_grad = False
        if self.linear.bias is not None:
            self.linear.bias.requires_grad = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        result = self.linear(x)
        lora_out = (self.dropout(x) @ self.lora_A.T) @ self.lora_B.T
        return result + (lora_out * self.scaling)


class LoRAMerger:
    """Merges LoRA adapter weights directly into original linear base weights."""

    @staticmethod
    def merge(adapter: LoRAAdapter) -> nn.Linear:
        with torch.no_grad():
            delta_w = (adapter.lora_B @ adapter.lora_A) * adapter.scaling
            adapter.linear.weight.data += delta_w
            adapter.linear.weight.requires_grad = True
        return adapter.linear
