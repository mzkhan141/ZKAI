"""Embeddings (TokenEmbedding, RotaryEmbedding/RoPE, PositionalEncoding, ALiBi)."""

import math
from typing import Optional, Tuple
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class TokenEmbedding(Module):
    """Maps token index sequence into continuous vector representation space."""

    def __init__(self, vocab_size: int, hidden_dim: int):
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self._torch_module = nn.Embedding(vocab_size, hidden_dim)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw.long()) * math.sqrt(self.hidden_dim))


class PositionalEncoding(Module):
    """Sinusoidal positional encoding for Non-Rotary Transformer architectures."""

    def __init__(self, hidden_dim: int, max_len: int = 5000):
        super().__init__()
        pe = torch.zeros(max_len, hidden_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, hidden_dim, 2).float() * (-math.log(10000.0) / hidden_dim))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def register_buffer(self, name: str, tensor: torch.Tensor) -> None:
        setattr(self, name, tensor)

    def forward(self, x: Tensor) -> Tensor:
        seq_len = x.shape[1]
        pe_slice = getattr(self, "pe")[:, :seq_len].to(x.raw.device)
        return Tensor(x.raw + pe_slice)


class RotaryEmbedding(Module):
    """Rotary Position Embedding (RoPE) applied directly to Query & Key projections."""

    def __init__(self, dim: int, max_position_embeddings: int = 4096, base: float = 10000.0):
        super().__init__()
        self.dim = dim
        self.base = base
        inv_freq = 1.0 / (self.base ** (torch.arange(0, self.dim, 2).float() / self.dim))
        self.register_buffer("inv_freq", inv_freq)

        t = torch.arange(max_position_embeddings, dtype=torch.float)
        freqs = torch.outer(t, inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos())
        self.register_buffer("sin_cached", emb.sin())

    def register_buffer(self, name: str, tensor: torch.Tensor) -> None:
        setattr(self, name, tensor)

    def _rotate_half(self, x: torch.Tensor) -> torch.Tensor:
        x1 = x[..., : x.shape[-1] // 2]
        x2 = x[..., x.shape[-1] // 2 :]
        return torch.cat((-x2, x1), dim=-1)

    def forward(self, q: torch.Tensor, k: torch.Tensor, seq_len: int) -> Tuple[torch.Tensor, torch.Tensor]:
        cos = getattr(self, "cos_cached")[:seq_len].to(q.device)
        sin = getattr(self, "sin_cached")[:seq_len].to(q.device)

        q_embed = (q * cos) + (self._rotate_half(q) * sin)
        k_embed = (k * cos) + (self._rotate_half(k) * sin)
        return q_embed, k_embed


class ALiBi(Module):
    """Attention with Linear Biases (ALiBi) penalty matrix generator."""

    def __init__(self, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        slopes = self._get_slopes(num_heads)
        self.register_buffer("slopes", slopes)

    def register_buffer(self, name: str, tensor: torch.Tensor) -> None:
        setattr(self, name, tensor)

    def _get_slopes(self, n: int) -> torch.Tensor:
        def get_slopes_power_of_2(n_val: int) -> list[float]:
            start = (2 ** (-2 ** -(math.log2(n_val) - 3)))
            ratio = start
            return [start * (ratio ** i) for i in range(n_val)]
        if math.log2(n).is_integer():
            return torch.tensor(get_slopes_power_of_2(n))
        else:
            closest_power_of_2 = 2 ** math.floor(math.log2(n))
            return torch.tensor(get_slopes_power_of_2(closest_power_of_2) + self._get_slopes(n - closest_power_of_2).tolist())

    def get_bias(self, seq_len: int, device: torch.device) -> torch.Tensor:
        slopes = getattr(self, "slopes").to(device)
        context_position = torch.arange(seq_len, device=device)[:, None]
        memory_position = torch.arange(seq_len, device=device)[None, :]
        relative_position = memory_position - context_position
        relative_position = torch.abs(relative_position).unsqueeze(0).expand(self.num_heads, -1, -1)
        return -slopes.view(self.num_heads, 1, 1) * relative_position
