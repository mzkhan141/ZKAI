"""WebCrawler and CrawlPolicy for multi-page web traversal."""

from dataclasses import dataclass
from typing import List, Set, Optional
import aiohttp
from bs4 import BeautifulSoup
from zkai.core.logger import get_logger

logger = get_logger("internet.crawler")


@dataclass
class CrawlPolicy:
    max_depth: int = 2
    max_pages: int = 20
    allowed_domains: Optional[List[str]] = None


class WebCrawler:
    """Multi-page recursive web crawler."""

    def __init__(self, policy: Optional[CrawlPolicy] = None):
        self.policy = policy or CrawlPolicy()
        self.visited: Set[str] = set()

    async def crawl(self, start_url: str) -> List[str]:
        logger.info(f"Starting web crawl from: {start_url}")
        urls_to_visit = [start_url]
        pages_content = []

        async with aiohttp.ClientSession() as session:
            while urls_to_visit and len(self.visited) < self.policy.max_pages:
                curr_url = urls_to_visit.pop(0)
                if curr_url in self.visited:
                    continue
                self.visited.add(curr_url)

                try:
                    async with session.get(curr_url, timeout=5) as resp:
                        if resp.status == 200:
                            html = await resp.text()
                            pages_content.append(html)
                except Exception as e:
                    logger.debug(f"Error crawling {curr_url}: {e}")

        return pages_content
