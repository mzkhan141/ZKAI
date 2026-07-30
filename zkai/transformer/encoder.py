"""Encoder Stack for Encoder-Decoder and Bidirectional Transformer Architectures."""

from typing import List, Optional
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor
from zkai.neural.normalization import RMSNorm
from zkai.transformer.embeddings import TokenEmbedding
from zkai.transformer.block import TransformerBlock


class Encoder(Module):
    """Transformer Encoder stack converting tokens into contextual sequence representations."""

    def __init__(
        self,
        vocab_size: int,
        hidden_dim: int,
        num_layers: int,
        num_heads: int,
        intermediate_dim: Optional[int] = None,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.embedding = TokenEmbedding(vocab_size, hidden_dim)
        self.layers = nn.ModuleList([
            TransformerBlock(hidden_dim, num_heads, intermediate_dim=intermediate_dim, dropout=dropout)._torch_module
            for _ in range(num_layers)
        ])
        self.norm = RMSNorm(hidden_dim)

    def forward(self, input_ids: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        h = self.embedding(input_ids)
        for layer in self.layers:
            # Wrap layer execution
            tb = TransformerBlock(h.shape[-1], 1)
            tb._torch_module = layer
            h = tb(h, mask=mask)
        return self.norm(h)
