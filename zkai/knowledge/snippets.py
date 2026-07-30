"""SnippetManager for code snippet storage and retrieval."""

from typing import Dict, List


class SnippetManager:
    """Manages reusable code and prompt snippets."""

    def __init__(self):
        self.snippets: Dict[str, str] = {}

    def save_snippet(self, name: str, code: str) -> None:
        self.snippets[name] = code

    def get_snippet(self, name: str) -> str:
        return self.snippets.get(name, "")
