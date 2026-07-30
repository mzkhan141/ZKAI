"""KVMemoryManager and PrefixCache for managing paged KV cache allocation and prefix sharing."""

from typing import Dict, List, Optional, Tuple
import torch
from zkai.core.logger import get_logger

logger = get_logger("transformer.kv_memory")


class PrefixCache:
    """Prefix-aware KV Cache reuse manager across distinct generation requests."""

    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.cache: Dict[Tuple[int, ...], torch.Tensor] = {}

    def get_prefix_kv(self, prefix_tokens: Tuple[int, ...]) -> Optional[torch.Tensor]:
        """Retrieves cached KV state for a common prefix token sequence."""
        return self.cache.get(prefix_tokens)

    def store_prefix_kv(self, prefix_tokens: Tuple[int, ...], kv_state: torch.Tensor) -> None:
        """Stores computed KV states for prefix token sequence."""
        if len(self.cache) >= self.max_entries:
            self.cache.pop(next(iter(self.cache)))
        self.cache[prefix_tokens] = kv_state


class KVMemoryManager:
    """Page-table KV cache memory allocator allocating and releasing fixed-size blocks."""

    def __init__(self, total_blocks: int = 1024, block_size: int = 16):
        self.total_blocks = total_blocks
        self.block_size = block_size
        self.free_blocks: List[int] = list(range(total_blocks))
        self.allocated_blocks: Dict[str, List[int]] = {}
        self.prefix_cache = PrefixCache()

    def allocate(self, request_id: str, num_tokens: int) -> List[int]:
        """Allocates physical blocks for a request sequence length."""
        needed_blocks = (num_tokens + self.block_size - 1) // self.block_size
        if len(self.free_blocks) < needed_blocks:
            logger.warning(f"KV Memory pressure: Out of KV blocks ({len(self.free_blocks)} available, {needed_blocks} requested)")
            needed_blocks = len(self.free_blocks)

        blocks = self.free_blocks[:needed_blocks]
        self.free_blocks = self.free_blocks[needed_blocks:]
        self.allocated_blocks[request_id] = blocks
        return blocks

    def free(self, request_id: str) -> None:
        """Frees all allocated KV blocks associated with request_id."""
        if request_id in self.allocated_blocks:
            blocks = self.allocated_blocks.pop(request_id)
            self.free_blocks.extend(blocks)
