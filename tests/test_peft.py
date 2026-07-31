"""Unit tests for PEFT subsystem."""

import pytest
import torch
import torch.nn as nn
from zkai.peft import (
    AdapterLayer,
    DoRAAdapter,
    IA3Adapter,
    LoRAAdapter,
    LoRAConfig,
    PrefixTuning,
    PromptTuning,
    QLoRAAdapter,
)


def test_lora_and_qlora():
    linear = nn.Linear(32, 32)
    cfg = LoRAConfig(r=4, lora_alpha=8.0)
    adapter = LoRAAdapter(linear, cfg)
    x = torch.randn(2, 32)
    out = adapter(x)
    assert out.shape == (2, 32)

    qadapter = QLoRAAdapter(nn.Linear(32, 32), cfg)
    qout = qadapter(x)
    assert qout.shape == (2, 32)


def test_adapter_and_ia3():
    ad = AdapterLayer(32, 8)
    x = torch.randn(2, 32)
    assert ad(x).shape == (2, 32)

    ia3 = IA3Adapter(32)
    assert ia3(x).shape == (2, 32)
