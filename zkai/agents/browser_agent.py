"""BrowserAgent specialized in web automation."""

from zkai.browser.search import BrowserSearch


class BrowserAgent:
    """Specialized Agent for headless browser navigation and scraping."""

    def __init__(self):
        self.search = BrowserSearch()

    def browse(self, url: str) -> str:
        return f"Browsing page: {url}"
