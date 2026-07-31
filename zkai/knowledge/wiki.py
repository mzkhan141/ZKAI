"""Wiki documentation vault with hyperlinked pages."""

from typing import Dict, List
from zkai.knowledge.base import KnowledgeEntry


class Wiki:
    """Markdown wiki page manager with bidirectional hyperlinking."""

    def __init__(self):
        self.pages: Dict[str, KnowledgeEntry] = {}

    def create_page(self, title: str, markdown_content: str, tags: List[str] = None) -> KnowledgeEntry:
        entry = KnowledgeEntry(id=title.lower().replace(" ", "_"), title=title, content=markdown_content, category="wiki", tags=tags or [])
        self.pages[entry.id] = entry
        return entry
