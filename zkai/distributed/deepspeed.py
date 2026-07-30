"""DeepSpeed integration wrapper."""

from typing import Any, Dict
from zkai.neural.module import Module
from zkai.core.logger import get_logger

logger = get_logger("distributed.deepspeed")


class DeepSpeedWrapper:
    """Wrapper providing DeepSpeed engine compatibility."""

    def __init__(self, model: Module, config: Dict[str, Any]):
        self.model = model
        self.config = config
        logger.info("Initialized DeepSpeedWrapper")
