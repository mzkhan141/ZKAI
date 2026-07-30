"""Transformer Block combining Attention, FeedForward, Normalization, and Residuals."""

from typing import Optional
from zkai.neural.module import Module
from zkai.neural.normalization import RMSNorm, LayerNorm
from zkai.neural.tensor import Tensor
from zkai.transformer.attention import MultiHeadAttention
from zkai.transformer.feedforward import FeedForward, MoEFeedForward
from zkai.transformer.kv_cache import KVCache


class TransformerBlock(Module):
    """Modern Pre-Norm Transformer Block with Attention & FeedForward/MoE sub-layers."""

    def __init__(
        self,
        hidden_dim: int,
        num_heads: int,
        num_kv_heads: Optional[int] = None,
        intermediate_dim: Optional[int] = None,
        dropout: float = 0.0,
        use_rmsnorm: bool = True,
        num_experts: int = 0,
    ):
        super().__init__()
        self.attn_norm = RMSNorm(hidden_dim) if use_rmsnorm else LayerNorm(hidden_dim)
        self.attn = MultiHeadAttention(hidden_dim, num_heads, num_kv_heads=num_kv_heads, dropout=dropout)

        self.ffn_norm = RMSNorm(hidden_dim) if use_rmsnorm else LayerNorm(hidden_dim)
        if num_experts > 0:
            self.ffn = MoEFeedForward(hidden_dim, intermediate_dim or hidden_dim * 4, num_experts=num_experts)
        else:
            self.ffn = FeedForward(hidden_dim, intermediate_dim=intermediate_dim, dropout=dropout)

    def forward(
        self,
        x: Tensor,
        kv_cache: Optional[KVCache] = None,
        start_pos: int = 0,
        mask: Optional[Tensor] = None,
    ) -> Tensor:
        # Pre-Norm Residual Attention
        normed_attn = self.attn_norm(x)
        h = x + self.attn(normed_attn, kv_cache=kv_cache, start_pos=start_pos, mask=mask)

        # Pre-Norm Residual FeedForward
        normed_ffn = self.ffn_norm(h)
        out = h + self.ffn(normed_ffn)
        return out
