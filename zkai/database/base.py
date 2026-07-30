"""Database Base Protocol."""

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional


class Database(ABC):
    """Abstract Base Class for Database connections."""

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def execute(self, query: str, params: Optional[tuple] = None) -> Any:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
