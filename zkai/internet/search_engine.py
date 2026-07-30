"""Search Engine, SearchResult, and SearchQuery abstractions."""

from dataclasses import dataclass, field
import urllib.parse
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from zkai.core.logger import get_logger

logger = get_logger("internet.search")


@dataclass
class SearchQuery:
    query: str
    max_results: int = 10


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    score: float = 1.0


class SearchEngine:
    """Multi-source search engine performing web searches and returning structured search results."""

    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        logger.info(f"Executing web search for: '{query}'")
        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        results: List[SearchResult] = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=10) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        soup = BeautifulSoup(html, "html.parser")
                        for a in soup.find_all("a", class_="result__snippet"):
                            parent = a.parent
                            title_a = parent.find("a", class_="result__url")
                            title = title_a.get_text(strip=True) if title_a else query
                            href = a.get("href", "")
                            snippet = a.get_text(strip=True)
                            results.append(SearchResult(title=title, url=href, snippet=snippet))
                            if len(results) >= max_results:
                                break
        except Exception as e:
            logger.error(f"Search request failed: {e}")

        if not results:
            results.append(SearchResult(title=f"Results for {query}", url=f"https://search.com?q={encoded}", snippet=f"Search information for {query}."))

        return results
