"""Unit tests for Quantization subsystem."""

import pytest
import torch
from zkai.quantization import FP8Quantizer, INT4Quantizer, NF4Quantizer, WeightPacker


def test_int4_quantization():
    t = torch.randn(4, 128)
    q, scale = INT4Quantizer.quantize_int4(t)
    deq = INT4Quantizer.dequantize_int4(q, scale)
    assert deq.shape == t.shape


def test_nf4_quantization():
    t = torch.randn(4, 4)
    indices, scale = NF4Quantizer.quantize_nf4(t)
    deq = NF4Quantizer.dequantize_nf4(indices, scale)
    assert deq.shape == t.shape


def test_weight_packer():
    int4_vals = torch.tensor([-5, 3, 0, 7], dtype=torch.int8)
    packed = WeightPacker.pack_int4_to_uint8(int4_vals)
    unpacked = WeightPacker.unpack_uint8_to_int4(packed, int4_vals.shape)
    assert torch.equal(int4_vals, unpacked)
