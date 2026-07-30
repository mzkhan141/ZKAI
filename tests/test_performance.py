"""Tests for Performance Optimization modules."""

import pytest
import asyncio
import torch
from zkai.core.lazy import LazyModule, LazyImport
from zkai.core.memory_pool import MemoryPool, ZeroCopyBuffer, StreamingBuffer
from zkai.core.async_io import AsyncBatchProcessor


def test_lazy_module():
    initialized = False

    def factory():
        nonlocal initialized
        initialized = True
        return lambda x: x * 2

    lazy = LazyModule(factory)
    assert initialized is False
    res = lazy(10)
    assert initialized is True
    assert res == 20


def test_memory_pool():
    pool = MemoryPool(buffer_shape=(10, 10), pool_size=4)
    buf = pool.acquire()
    assert buf.shape == (10, 10)
    pool.release(buf)
    assert len(pool.free_buffers) == 4


def test_async_batch_processor():
    processor = AsyncBatchProcessor(max_concurrency=2)
    items = [1, 2, 3, 4]
    results = asyncio.run(processor.process_batch_async(items, lambda x: x ** 2))
    assert results == [1, 4, 9, 16]
