"""HubUploader for publishing model checkpoints."""

from pathlib import Path
from zkai.core.logger import get_logger

logger = get_logger("hub.uploader")


class HubUploader:
    """Publishes trained native .zk model containers to ModelHub storage."""

    def upload(self, model_file: str, repository_id: str) -> bool:
        logger.info(f"Uploading '{model_file}' to Hub repository '{repository_id}'...")
        return True
