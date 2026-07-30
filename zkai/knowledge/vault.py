"""MarkdownVault for file-backed Obsidian-style markdown notes."""

from pathlib import Path
from typing import List


class MarkdownVault:
    """Manages local folder of markdown note files."""

    def __init__(self, vault_dir: str = "./vault"):
        self.vault_dir = Path(vault_dir)
        self.vault_dir.mkdir(parents=True, exist_ok=True)

    def list_notes(self) -> List[str]:
        return [p.stem for p in self.vault_dir.glob("*.md")]

    def read_note(self, title: str) -> str:
        p = self.vault_dir / f"{title}.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def write_note(self, title: str, content: str) -> None:
        p = self.vault_dir / f"{title}.md"
        p.write_text(content, encoding="utf-8")
