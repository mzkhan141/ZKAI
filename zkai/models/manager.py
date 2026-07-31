"""ModelManager orchestrating model discovery, loading, device placement, and caching."""

from typing import Any, Dict, List, Optional
from zkai.models.loader import ModelLoader
from zkai.models.registry import ModelRegistry
from zkai.models.downloader import ModelDownloader
from zkai.models.cache import ModelCache
from zkai.models.converter import ModelConverter
from zkai.models.checkpoint import ModelCheckpointManager
from zkai.core.backend import DeviceManager
from zkai.core.logger import get_logger

logger = get_logger("models.manager")


class ModelManager:
    """Master Model Subsystem Orchestrator for ZKAI."""

    def __init__(self):
        self.loader = ModelLoader()
        self.registry = ModelRegistry()
        self.downloader = ModelDownloader()
        self.cache = ModelCache()
        self.converter = ModelConverter()
        self.checkpoints = ModelCheckpointManager()

    def load(self, model_name_or_path: str, device: str = "auto") -> Any:
        """Loads model into memory or retrieves from cache."""
        target_device = DeviceManager.get_optimal_device() if device == "auto" else device
        cached = self.cache.get(model_name_or_path)
        if cached is not None:
            return cached

        resolved_path = self.registry.resolve(model_name_or_path) or model_name_or_path
        weights, meta = self.loader.load(resolved_path, device=target_device)

        self.cache.put(model_name_or_path, weights)
        logger.info(f"Loaded model '{model_name_or_path}' onto device '{target_device}'")
        return weights

    def save(self, model: Any, file_path: str) -> str:
        """Saves model to native .zk format container file."""
        if hasattr(model, "state_dict"):
            state_dict = model.state_dict()
        elif isinstance(model, dict):
            state_dict = model
        else:
            state_dict = {}

        return self.converter.pytorch_to_zk(file_path, file_path)
