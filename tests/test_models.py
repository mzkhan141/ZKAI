"""Unit tests for zkai.models management subsystem."""

import pytest
import torch
from zkai.models.metadata import ModelMetadata
from zkai.models.registry import ModelRegistry
from zkai.models.format_zk import ZKModelFormat
from zkai.models.quantization import Quantizer


def test_model_registry():
    registry = ModelRegistry()
    registry.register("test_model", "path/to/model.zk")
    assert registry.resolve("test_model") == "path/to/model.zk"


def test_quantizer():
    tensor = torch.randn(10, 10)
    q_tensor, scale = Quantizer.quantize_int8(tensor)
    assert q_tensor.dtype == torch.int8
    dequant = Quantizer.dequantize_int8(q_tensor, scale)
    assert dequant.shape == (10, 10)


def test_zk_model_format(temp_dir):
    file_path = str(temp_dir / "test_saved_model.zk")
    state_dict = {"weight": torch.randn(4, 4)}
    meta = ModelMetadata(
        name="TestZK",
        architecture="Transformer",
        num_parameters=16,
        vocab_size=100,
        hidden_dim=4,
        num_layers=1,
        num_heads=1,
    )
    ZKModelFormat.save_model(file_path, state_dict, meta)
    loaded_meta, _ = ZKModelFormat.load_model(file_path)
    assert loaded_meta.name == "TestZK"
