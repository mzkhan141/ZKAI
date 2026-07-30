"""Tests for High Performance Inference Engine modules."""

import pytest
from zkai.transformer.continuous_batcher import ContinuousBatcher, DynamicBatchScheduler, SequenceScheduler
from zkai.transformer.kv_memory import KVMemoryManager, PrefixCache
from zkai.transformer.token_streamer import TokenStreamer, StreamingGeneration


def test_continuous_batcher():
    batcher = ContinuousBatcher(max_batch_size=2)
    req1 = batcher.add_request("req1", [1, 2, 3], max_new_tokens=5)
    req2 = batcher.add_request("req2", [4, 5], max_new_tokens=5)
    active = batcher.step()
    assert len(active) >= 1


def test_kv_memory_manager():
    kv_mgr = KVMemoryManager(total_blocks=100, block_size=16)
    blocks = kv_mgr.allocate("req1", num_tokens=32)
    assert len(blocks) == 2
    kv_mgr.free("req1")
    assert len(kv_mgr.free_blocks) == 100


def test_prefix_cache():
    cache = PrefixCache()
    import torch
    cache.store_prefix_kv((1, 2, 3), torch.tensor([1.0]))
    val = cache.get_prefix_kv((1, 2, 3))
    assert val is not None


def test_token_streamer():
    streamer = TokenStreamer()
    streamer.put("Hello ")
    streamer.put("World")
    streamer.end()

    tokens = list(streamer)
    assert tokens == ["Hello ", "World"]
