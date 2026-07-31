"""Playwright Browser Automation (Browser, Tab, Page) with fallback."""

from typing import Any, Optional, List
import asyncio
from zkai.core.logger import get_logger

try:
    from playwright.async_api import async_playwright, Browser as PWBrowser, Page as PWPage
except ImportError:
    async_playwright = None
    PWBrowser = None
    PWPage = None

logger = get_logger("browser")


class Page:
    """Wrapped Browser Page automation interface."""

    def __init__(self, pw_page: Optional[Any] = None):
        self._page = pw_page

    async def goto(self, url: str) -> None:
        logger.info(f"Navigating browser to: {url}")
        if self._page:
            await self._page.goto(url)

    async def content(self) -> str:
        if self._page:
            return await self._page.content()
        return "<html><body>Browser fallback content</body></html>"

    async def title(self) -> str:
        if self._page:
            return await self._page.title()
        return "Fallback Page Title"

    async def screenshot(self, path: str) -> None:
        if self._page:
            await self._page.screenshot(path=path)

    async def click(self, selector_or_coords: str) -> None:
        if self._page:
            await self._page.click(selector_or_coords)


class Tab(Page):
    """Tab alias."""
    pass


class Browser:
    """Headless browser automation controller powered by Playwright with fallback."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self._playwright = None
        self._browser = None

    async def start(self) -> None:
        if not self._browser and async_playwright:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=self.headless)

    async def open(self, url: str) -> Page:
        await self.start()
        if self._browser:
            pw_page = await self._browser.new_page()
            page = Page(pw_page)
            await page.goto(url)
            return page
        return Page(None)

    async def close(self) -> None:
        if self._browser:
            await self._browser.close()
            await self._playwright.stop()
            self._browser = None
