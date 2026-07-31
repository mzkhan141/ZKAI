"""IA3 (Infused Adapter by Inhibiting and Amplifying Inner Activations)."""

import torch
import torch.nn as nn


class IA3Adapter(nn.Module):
    """Rescales inner activations of keys, values, and feedforward networks via learned vector."""

    def __init__(self, in_features: int):
        super().__init__()
        self.ia3_vector = nn.Parameter(torch.ones(in_features))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x * self.ia3_vector
