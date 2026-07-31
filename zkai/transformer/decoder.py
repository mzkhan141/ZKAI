"""Decoder-only Causal Autoregressive Transformer Architecture."""

from typing import List, Optional
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor
from zkai.neural.normalization import RMSNorm
from zkai.transformer.embeddings import TokenEmbedding
from zkai.transformer.block import TransformerBlock
from zkai.transformer.kv_cache import KVCache
from zkai.core.config import TransformerConfig


class Decoder(Module):
    """Decoder-only Causal Transformer for native ZKAI Foundation Models."""

    def __init__(self, config: Optional[TransformerConfig] = None, **kwargs):
        super().__init__()
        self.config = config or TransformerConfig(**kwargs)

        self.tok_embeddings = TokenEmbedding(self.config.vocab_size, self.config.hidden_dim)
        self.blocks: List[TransformerBlock] = [
            TransformerBlock(
                hidden_dim=self.config.hidden_dim,
                num_heads=self.config.num_heads,
                num_kv_heads=self.config.num_kv_heads,
                intermediate_dim=self.config.intermediate_dim,
                dropout=self.config.dropout,
                num_experts=self.config.num_experts,
            )
            for _ in range(self.config.num_layers)
        ]
        # Also register as nn.ModuleList for parameter tracking
        self._torch_module = nn.Module()
        self._torch_module.tok_embeddings = self.tok_embeddings._torch_module
        block_torch_modules = []
        for b in self.blocks:
            # Build a nn.Module container for each block's sub-modules
            block_mod = nn.Module()
            block_mod.attn_q = b.attn.q_proj
            block_mod.attn_k = b.attn.k_proj
            block_mod.attn_v = b.attn.v_proj
            block_mod.attn_o = b.attn.o_proj
            block_torch_modules.append(block_mod)
        self._torch_module.blocks = nn.ModuleList(block_torch_modules)

        self.norm = RMSNorm(self.config.hidden_dim, eps=self.config.layer_norm_eps)
        self.output_head = nn.Linear(self.config.hidden_dim, self.config.vocab_size, bias=False)
        self._torch_module.output_head = self.output_head

    def forward(
        self,
        input_ids: Tensor,
        start_pos: int = 0,
        kv_caches: Optional[List[KVCache]] = None,
    ) -> Tensor:
        bsz, seqlen = input_ids.shape
        h = self.tok_embeddings(input_ids)

        for idx, block in enumerate(self.blocks):
            cache = kv_caches[idx] if kv_caches and idx < len(kv_caches) else None
            h = block(h, kv_cache=cache, start_pos=start_pos)

        h = self.norm(h)
        logits = self.output_head(h.raw)
        return Tensor(logits)
