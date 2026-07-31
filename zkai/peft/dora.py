"""Weight-Decomposed Low-Rank Adaptation (DoRA)."""

import torch
import torch.nn as nn
from zkai.models.lora import LoRAAdapter, LoRAConfig


class DoRAAdapter(LoRAAdapter):
    """DoRA decouples directional weight update from magnitude adjustment."""

    def __init__(self, linear_layer: nn.Linear, config: LoRAConfig):
        super().__init__(linear_layer, config)
        self.magnitude = nn.Parameter(torch.norm(linear_layer.weight.data, dim=1, keepdim=True))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = super().forward(x)
        norm = torch.norm(out, dim=-1, keepdim=True)
        norm = torch.where(norm == 0, torch.ones_like(norm), norm)
        return (out / norm) * self.magnitude.T
