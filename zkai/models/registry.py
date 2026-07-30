"""ModelRegistry for model discovery, registration, and path resolution."""

from typing import Dict, List, Optional, Any
from zkai.models.metadata import ModelMetadata
from zkai.core.logger import get_logger

logger = get_logger("models.registry")


class ModelRegistry:
    """Registry maintaining active registered model architectures and weights locations."""

    def __init__(self):
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, path_or_uri: str, metadata: Optional[ModelMetadata] = None) -> None:
        self._registry[name] = {
            "path": path_or_uri,
            "metadata": metadata,
        }
        logger.info(f"Registered model '{name}' -> {path_or_uri}")

    def resolve(self, name: str) -> Optional[str]:
        if name in self._registry:
            return self._registry[name]["path"]
        return None

    def list_models(self) -> List[str]:
        return list(self._registry.keys())
