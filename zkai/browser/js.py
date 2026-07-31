"""JavaScript Execution Engine using Playwright."""

from typing import Any
from zkai.browser.browser import Page


class JSExecutor:
    """Executes arbitrary JavaScript snippets inside active Playwright browser pages."""

    async def execute_js(self, page: Page, script: str) -> Any:
        return await page._page.evaluate(script)
