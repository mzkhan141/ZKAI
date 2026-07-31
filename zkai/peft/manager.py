"""AdapterManager for storing, loading, and hot-swapping PEFT adapters."""

from typing import Dict, Optional
import torch.nn as nn


class AdapterManager:
    """Registry managing active task-specific fine-tuned adapters."""

    def __init__(self):
        self.adapters: Dict[str, nn.Module] = {}
        self.active_adapter: Optional[str] = None

    def register_adapter(self, name: str, adapter: nn.Module) -> None:
        self.adapters[name] = adapter
        if self.active_adapter is None:
            self.active_adapter = name

    def set_active(self, name: str) -> None:
        if name in self.adapters:
            self.active_adapter = name
