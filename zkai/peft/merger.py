"""AdapterMerger for combining PEFT weights with base models."""

import torch.nn as nn
from zkai.models.lora import LoRAAdapter, LoRAMerger


class AdapterMerger:
    """Merges trained PEFT adapters into base model layers for zero-overhead inference."""

    @staticmethod
    def merge_adapter(adapter: LoRAAdapter) -> nn.Linear:
        return LoRAMerger.merge(adapter)
