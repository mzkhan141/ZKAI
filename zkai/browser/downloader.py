"""Downloader for downloading web resources and media files."""

from pathlib import Path
import aiohttp
from zkai.core.logger import get_logger

logger = get_logger("browser.downloader")


class Downloader:
    """Async file downloader for web pages and media assets."""

    async def download_file(self, url: str, output_path: str) -> str:
        logger.info(f"Downloading {url} -> {output_path}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()
                path = Path(output_path)
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "wb") as f:
                    f.write(content)
        return output_path
