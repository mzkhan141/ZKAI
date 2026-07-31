"""ResearchAgent specialized in web search and fact gathering."""

from zkai.internet.search_engine import SearchEngine


class ResearchAgent:
    """Specialized Agent for web searching and information collection."""

    def __init__(self):
        self.search_engine = SearchEngine()

    def research(self, query: str):
        return f"Research results for: {query}"
