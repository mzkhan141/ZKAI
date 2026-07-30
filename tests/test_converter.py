"""Tests for universal ModelConverter, WeightValidator, and MetadataConverter."""

import pytest
import torch
from zkai.models.converter import ModelConverter
from zkai.models.compatibility_checker import CompatibilityChecker
from zkai.models.metadata_converter import MetadataConverter
from zkai.models.weight_validator import WeightValidator
from zkai.models.metadata import ModelMetadata
from zkai.core.types import ModelFormat


def test_compatibility_checker():
    checker = CompatibilityChecker()
    assert checker.check_compatibility(ModelFormat.PYTORCH, ModelFormat.ZK) is True


def test_metadata_converter():
    meta = ModelMetadata(name="test_m", architecture="Decoder", num_parameters=100)
    gguf_m = MetadataConverter.to_gguf_metadata(meta)
    assert gguf_m["general.name"] == "test_m"

    hf_cfg = {"architectures": ["LlamaForCausalLM"], "vocab_size": 32000, "hidden_size": 4096}
    meta_from_hf = MetadataConverter.from_hf_config(hf_cfg)
    assert meta_from_hf.vocab_size == 32000


def test_weight_validator():
    validator = WeightValidator()
    clean_state = {"weight": torch.randn(10, 10)}
    is_valid, issues = validator.validate_weights(clean_state)
    assert is_valid is True

    nan_state = {"weight": torch.tensor([float("nan")])}
    is_valid_nan, issues_nan = validator.validate_weights(nan_state)
    assert is_valid_nan is False
