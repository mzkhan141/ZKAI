"""DOM Inspector for analyzing HTML element trees."""

from typing import Dict, List, Any
from bs4 import BeautifulSoup


class DOMInspector:
    """Inspects and queries DOM elements."""

    def inspect_selectors(self, html: str, selector: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(selector)
        return [el.get_text() for el in elements]
