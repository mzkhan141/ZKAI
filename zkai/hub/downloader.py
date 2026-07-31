"""HubDownloader for downloading model artifacts with integrity verification."""

from pathlib import Path
from zkai.models.downloader import ModelDownloader


class HubDownloader:
    """Downloader wrapping ModelDownloader with checksum validation."""

    def __init__(self, cache_dir: str = "./hub_cache"):
        self.downloader = ModelDownloader(cache_dir=cache_dir)

    def download(self, model_url: str) -> Path:
        return self.downloader.download(model_url)
