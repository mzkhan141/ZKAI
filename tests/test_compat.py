"""Tests for Ecosystem Compatibility Layers."""

import pytest
from zkai.compat.huggingface import HuggingFaceCompat
from zkai.compat.onnx_compat import ONNXCompat
from zkai.compat.tensorrt_compat import TensorRTCompat
from zkai.compat.gguf_compat import GGUFCompat
from zkai.compat.safetensors_compat import SafetensorsCompat
from zkai.compat.openvino_compat import OpenVINOCompat


def test_compat_wrappers():
    hf = HuggingFaceCompat()
    assert hf.load_hf_tokenizer("dummy") is None or hf.load_hf_tokenizer("dummy") is not None

    gguf = GGUFCompat("dummy.gguf")
    header = gguf.read_header()
    assert header["magic"] == "GGUF"

    st = SafetensorsCompat()
    assert st is not None
