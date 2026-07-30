"""PDFLibrary indexing and loading PDF academic documents."""

from pathlib import Path
from typing import List
from zkai.documents.loader import DocumentLoader


class PDFLibrary:
    """PDF document collection indexer."""

    def __init__(self, pdf_dir: str = "./pdf_library"):
        self.pdf_dir = Path(pdf_dir)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.loader = DocumentLoader()

    def list_pdfs(self) -> List[str]:
        return [str(p) for p in self.pdf_dir.glob("*.pdf")]
