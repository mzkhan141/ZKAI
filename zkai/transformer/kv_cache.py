"""KV Cache and Paged KV Cache infrastructure for fast autoregressive inference."""

from typing import Tuple, Optional
import torch


class KVCache:
    """Key-Value Cache maintaining key and value tensors across decoding steps."""

    def __init__(self, max_batch_size: int, max_seq_len: int, num_kv_heads: int, head_dim: int, device: str = "cpu", dtype: torch.dtype = torch.float32):
        self.max_seq_len = max_seq_len
        self.k_cache = torch.zeros((max_batch_size, num_kv_heads, max_seq_len, head_dim), device=device, dtype=dtype)
        self.v_cache = torch.zeros((max_batch_size, num_kv_heads, max_seq_len, head_dim), device=device, dtype=dtype)
        self.seq_len = 0

    def update(self, key_states: torch.Tensor, value_states: torch.Tensor, start_pos: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Appends new token keys & values into cache buffers and returns full context view."""
        bsz, num_heads, seq_len, head_dim = key_states.shape
        self.k_cache[:bsz, :, start_pos : start_pos + seq_len, :] = key_states
        self.v_cache[:bsz, :, start_pos : start_pos + seq_len, :] = value_states
        self.seq_len = start_pos + seq_len

        return (
            self.k_cache[:bsz, :, : self.seq_len, :],
            self.v_cache[:bsz, :, : self.seq_len, :],
        )

    def reset(self) -> None:
        self.k_cache.zero_()
        self.v_cache.zero_()
        self.seq_len = 0


class PagedKVCache(KVCache):
    """Paged Memory KV Cache (vLLM style block allocation strategy)."""

    def __init__(self, block_size: int = 16, num_blocks: int = 128, **kwargs):
        super().__init__(**kwargs)
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.block_table: dict[int, list[int]] = {}
