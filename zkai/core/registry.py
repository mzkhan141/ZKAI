"""Generic Component Registry pattern implementation."""

from typing import Any, Dict, Type, TypeVar, Optional, List
from zkai.core.exceptions import ZKAIError
from zkai.core.logger import get_logger

logger = get_logger("registry")

T = TypeVar("T")


class Registry(Dict[str, Type[T]]):
    """Generic Registry mapping string identifiers to registered class types."""

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def register(self, name: Optional[str] = None) -> Any:
        """Decorator or direct call to register a class type."""
        def _register(cls: Type[T]) -> Type[T]:
            key = name or cls.__name__
            if key in self:
                logger.warning(f"Overwriting registry key '{key}' in '{self.name}'")
            self[key] = cls
            logger.debug(f"Registered '{key}' -> '{cls.__name__}' in registry '{self.name}'")
            return cls
        return _register

    def get_class(self, key: str) -> Type[T]:
        if key not in self:
            raise ZKAIError(f"Key '{key}' not found in Registry '{self.name}'. Available: {list(self.keys())}")
        return self[key]

    def list_keys(self) -> List[str]:
        return list(self.keys())
