"""Prefix Tuning prependable key-value embeddings."""

import torch
import torch.nn as nn


class PrefixTuning(nn.Module):
    """Prepends learnable continuous prefix key/value tokens to transformer attention."""

    def __init__(self, prefix_length: int = 10, hidden_dim: int = 768):
        super().__init__()
        self.prefix_length = prefix_length
        self.prefix_embedding = nn.Parameter(torch.randn(prefix_length, hidden_dim))

    def forward(self, batch_size: int) -> torch.Tensor:
        return self.prefix_embedding.unsqueeze(0).expand(batch_size, -1, -1)
