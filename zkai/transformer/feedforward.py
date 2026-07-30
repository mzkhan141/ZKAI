"""FeedForward and Mixture-of-Experts (MoE) Networks for Transformers."""

from typing import List, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class FeedForward(Module):
    """Gated SwiGLU FeedForward Network (LLaMA / Mistral standard)."""

    def __init__(self, hidden_dim: int, intermediate_dim: Optional[int] = None, dropout: float = 0.0):
        super().__init__()
        if intermediate_dim is None:
            intermediate_dim = int(2 * (4 * hidden_dim) / 3)

        self.w1 = nn.Linear(hidden_dim, intermediate_dim, bias=False)  # gate
        self.w2 = nn.Linear(intermediate_dim, hidden_dim, bias=False)  # down
        self.w3 = nn.Linear(hidden_dim, intermediate_dim, bias=False)  # up
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor) -> Tensor:
        # SwiGLU: (silu(w1(x)) * w3(x)) @ w2
        swish = F.silu(self.w1(x.raw))
        gated = swish * self.w3(x.raw)
        return Tensor(self.dropout(self.w2(gated)))


class GatedFeedForward(FeedForward):
    """Gated FeedForward Alias."""
    pass


class MoEFeedForward(Module):
    """Mixture-of-Experts (MoE) FeedForward layer with top-k router gating."""

    def __init__(self, hidden_dim: int, intermediate_dim: int, num_experts: int = 8, num_experts_per_tok: int = 2):
        super().__init__()
        self.num_experts = num_experts
        self.num_experts_per_tok = num_experts_per_tok
        self.gate = nn.Linear(hidden_dim, num_experts, bias=False)
        self.experts = nn.ModuleList([FeedForward(hidden_dim, intermediate_dim)._torch_module for _ in range(num_experts)])

    def forward(self, x: Tensor) -> Tensor:
        bsz, seq_len, hidden_dim = x.shape
        x_flat = x.raw.view(-1, hidden_dim)

        router_logits = self.gate(x_flat)
        routing_weights = F.softmax(router_logits, dim=-1)
        topk_weights, topk_indices = torch.topk(routing_weights, self.num_experts_per_tok, dim=-1)
        topk_weights = topk_weights / topk_weights.sum(dim=-1, keepdim=True)

        final_output = torch.zeros_like(x_flat)
        for i, expert in enumerate(self.experts):
            batch_idx, nth_expert = torch.where(topk_indices == i)
            if batch_idx.numel() == 0:
                continue
            expert_tokens = x_flat[batch_idx]
            expert_out = expert(expert_tokens)
            weight = topk_weights[batch_idx, nth_expert].unsqueeze(-1)
            final_output.index_add_(0, batch_idx, expert_out * weight)

        return Tensor(final_output.view(bsz, seq_len, hidden_dim))
