"""ModelCache for RAM/VRAM model lifecycle and LRU eviction management."""

from typing import Dict, Any, Optional
import torch
from zkai.core.logger import get_logger

logger = get_logger("models.cache")


class ModelCache:
    """Manages loaded model instances in GPU VRAM and CPU RAM."""

    def __init__(self, max_loaded_models: int = 3):
        self.max_loaded_models = max_loaded_models
        self._loaded_models: Dict[str, Any] = {}

    def put(self, name: str, model: Any) -> None:
        if len(self._loaded_models) >= self.max_loaded_models:
            evict_name = next(iter(self._loaded_models))
            logger.info(f"Evicting model '{evict_name}' from VRAM memory cache")
            del self._loaded_models[evict_name]
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        self._loaded_models[name] = model

    def get(self, name: str) -> Optional[Any]:
        return self._loaded_models.get(name)

    def clear(self) -> None:
        self._loaded_models.clear()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
