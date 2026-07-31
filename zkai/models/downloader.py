"""Model Downloader for fetching weights from HF Hub and HTTP mirrors."""

from pathlib import Path
import urllib.request
from typing import Optional
from zkai.core.logger import get_logger

logger = get_logger("models.downloader")


class ModelDownloader:
    """Downloader fetching model weight files and tokenizers."""

    def __init__(self, cache_dir: str = "./model_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download_file(self, url: str, filename: Optional[str] = None) -> str:
        name = filename or url.split("/")[-1]
        target_path = self.cache_dir / name

        if target_path.exists():
            logger.info(f"Model file already exists in cache: {target_path}")
            return str(target_path)

        logger.info(f"Downloading model artifact from {url}...")
        urllib.request.urlretrieve(url, target_path)
        logger.info(f"Successfully downloaded to {target_path}")
        return str(target_path)
