"""Notebook for interactive research logs."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class NotebookCell:
    cell_type: str  # code or markdown
    source: str


class Notebook:
    """Interactive notebook storing code cells and markdown explanations."""

    def __init__(self, name: str):
        self.name = name
        self.cells: List[NotebookCell] = []

    def add_cell(self, cell_type: str, source: str) -> None:
        self.cells.append(NotebookCell(cell_type=cell_type, source=source))
