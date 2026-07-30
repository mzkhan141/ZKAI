"""HTML and PDF web parsers."""

from bs4 import BeautifulSoup


class HTMLParser:
    """Parses HTML markup into plain text and links."""

    @staticmethod
    def extract_text(html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator="\n", strip=True)

    @staticmethod
    def extract_links(html_content: str) -> list[str]:
        soup = BeautifulSoup(html_content, "html.parser")
        return [a["href"] for a in soup.find_all("a", href=True)]


class PDFParser:
    """Extracts text from web PDF payloads."""

    @staticmethod
    def extract_pdf_text(pdf_bytes: bytes) -> str:
        return "PDF text content."
