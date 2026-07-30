"""Bottleneck Adapter layers (Pfeiffer / Houlsby architecture)."""

import torch
import torch.nn as nn


class AdapterLayer(nn.Module):
    """Bottleneck adapter layer inserted after feed-forward or attention blocks."""

    def __init__(self, in_features: int, bottleneck_dim: int = 64):
        super().__init__()
        self.down_proj = nn.Linear(in_features, bottleneck_dim)
        self.act = nn.GELU()
        self.up_proj = nn.Linear(bottleneck_dim, in_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        res = self.up_proj(self.act(self.down_proj(x)))
        return x + res
