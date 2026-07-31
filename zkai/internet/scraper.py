"""WebScraper and ContentExtractor for extracting clean page content."""

from bs4 import BeautifulSoup
import aiohttp
from zkai.core.logger import get_logger

logger = get_logger("internet.scraper")


class ContentExtractor:
    """Extracts main body text content from HTML markup while discarding boilerplate."""

    @staticmethod
    def extract_main_text(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        return soup.get_text(separator="\n", strip=True)


class WebScraper:
    """Scrapes raw web pages and extracts structured text contents."""

    async def scrape(self, url: str) -> str:
        logger.info(f"Scraping web page: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                html = await resp.text()
                return ContentExtractor.extract_main_text(html)
