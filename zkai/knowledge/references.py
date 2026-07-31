"""ReferenceManager for academic paper citations and references."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Reference:
    cite_key: str
    title: str
    authors: List[str]
    year: int
    doi: str = ""


class ReferenceManager:
    """Manages BibTeX and academic paper references."""

    def __init__(self):
        self.references: Dict[str, Reference] = {}

    def add_reference(self, ref: Reference) -> None:
        self.references[ref.cite_key] = ref

    def get_reference(self, cite_key: str) -> str:
        ref = self.references.get(cite_key)
        if not ref:
            return ""
        return f"{', '.join(ref.authors)} ({ref.year}). {ref.title}."
