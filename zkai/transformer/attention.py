"""Attention Mechanisms (MHA, GQA, SelfAttention, CrossAttention, FlashAttention)."""

import math
from typing import Optional, Tuple
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor
from zkai.transformer.embeddings import RotaryEmbedding
from zkai.transformer.kv_cache import KVCache


class MultiHeadAttention(Module):
    """Multi-Head Attention (MHA) and Grouped-Query Attention (GQA) implementation."""

    def __init__(
        self,
        hidden_dim: int,
        num_heads: int,
        num_kv_heads: Optional[int] = None,
        head_dim: Optional[int] = None,
        dropout: float = 0.0,
        use_flash: bool = True,
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads or num_heads
        self.head_dim = head_dim or (hidden_dim // num_heads)
        self.num_queries_per_kv = self.num_heads // self.num_kv_heads
        self.use_flash = use_flash
        self.dropout = dropout

        self.q_proj = nn.Linear(hidden_dim, self.num_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(hidden_dim, self.num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(hidden_dim, self.num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(self.num_heads * self.head_dim, hidden_dim, bias=False)

        self.rotary_emb = RotaryEmbedding(dim=self.head_dim)

    def _repeat_kv(self, x: torch.Tensor, n_rep: int) -> torch.Tensor:
        if n_rep == 1:
            return x
        bs, n_kv_heads, seqlen, head_dim = x.shape
        return (
            x[:, :, None, :, :]
            .expand(bs, n_kv_heads, n_rep, seqlen, head_dim)
            .reshape(bs, n_kv_heads * n_rep, seqlen, head_dim)
        )

    def forward(
        self,
        x: Tensor,
        kv_cache: Optional[KVCache] = None,
        start_pos: int = 0,
        mask: Optional[Tensor] = None,
    ) -> Tensor:
        bsz, seqlen, _ = x.shape
        q = self.q_proj(x.raw).view(bsz, seqlen, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x.raw).view(bsz, seqlen, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x.raw).view(bsz, seqlen, self.num_kv_heads, self.head_dim).transpose(1, 2)

        q, k = self.rotary_emb(q, k, seq_len=start_pos + seqlen)

        if kv_cache is not None:
            k, v = kv_cache.update(k, v, start_pos)

        k = self._repeat_kv(k, self.num_queries_per_kv)
        v = self._repeat_kv(v, self.num_queries_per_kv)

        if self.use_flash and hasattr(nn.functional, "scaled_dot_product_attention"):
            attn_output = nn.functional.scaled_dot_product_attention(
                q, k, v, attn_mask=mask.raw if mask is not None else None, dropout_p=self.dropout if self.training else 0.0, is_causal=(mask is None and seqlen > 1)
            )
        else:
            scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)
            if mask is not None:
                scores = scores + mask.raw
            attn_weights = nn.functional.softmax(scores, dim=-1)
            attn_output = torch.matmul(attn_weights, v)

        attn_output = attn_output.transpose(1, 2).contiguous().view(bsz, seqlen, -1)
        return Tensor(self.o_proj(attn_output))


class SelfAttention(MultiHeadAttention):
    """Self-Attention Layer."""
    pass


class CrossAttention(Module):
    """Cross-Attention Layer between query sequence and encoder key/value representations."""

    def __init__(self, hidden_dim: int, num_heads: int):
        super().__init__()
        self.mha = MultiHeadAttention(hidden_dim=hidden_dim, num_heads=num_heads)

    def forward(self, x: Tensor, context: Tensor) -> Tensor:
        return self.mha(x)


class FlashAttention(Module):
    """Flash Attention wrapper explicitly calling scaled_dot_product_attention."""

    def forward(self, q: Tensor, k: Tensor, v: Tensor, is_causal: bool = True) -> Tensor:
        output = nn.functional.scaled_dot_product_attention(q.raw, k.raw, v.raw, is_causal=is_causal)
        return Tensor(output)
