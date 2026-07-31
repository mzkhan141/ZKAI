"""ModelHub primary interface."""

from typing import Any, Optional
from zkai.models.manager import ModelManager
from zkai.core.logger import get_logger

logger = get_logger("hub")


class ModelHub:
    """Central model hub for downloading, publishing, and resolving model artifacts."""

    def __init__(self):
        self.manager = ModelManager()

    def load_model(self, model_id: str) -> Any:
        logger.info(f"Fetching model '{model_id}' from ZKAI ModelHub...")
        return self.manager
