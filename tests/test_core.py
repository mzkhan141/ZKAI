"""Unit tests for zkai.core infrastructure."""

import pytest
from zkai.core.types import DeviceType, DType, BackendType, TaskStatus
from zkai.core.exceptions import ZKAIError, BackendError
from zkai.core.cache import LRUCache, TTLCache
from zkai.core.serialization import ZKSerializer, ZKHeader


def test_core_types():
    assert DeviceType.CPU.value == "cpu"
    assert DType.FLOAT32.value == "float32"
    assert BackendType.PYTORCH.value == "pytorch"
    assert TaskStatus.PENDING.value == "pending"


def test_core_exceptions():
    err = ZKAIError("Test error", details={"code": 500})
    assert err.message == "Test error"
    assert err.details["code"] == 500


def test_lru_cache():
    cache = LRUCache(capacity=2)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    cache.set("c", 3)
    # "b" should be evicted
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_zk_serializer(temp_dir):
    file_path = str(temp_dir / "test_model.zk")
    header = ZKHeader(
        model_name="TestModel",
        architecture="Decoder",
        parameter_count=1000,
    )
    payload = b"hello_tensor_bytes"
    ZKSerializer.write_zk_file(file_path, header, payload)

    loaded_header, loaded_payload, _ = ZKSerializer.read_zk_file(file_path)
    assert loaded_header.model_name == "TestModel"
    assert loaded_payload == payload
