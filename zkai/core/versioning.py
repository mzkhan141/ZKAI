"""API Versioning, Deprecation handling, and Serialization Backward Compatibility layer."""

import warnings
from typing import Any, Callable, Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("core.versioning")


class APIVersion:
    """Semantic Versioning (SemVer) tracking container."""

    MAJOR = 1
    MINOR = 0
    PATCH = 0

    @classmethod
    def get_version_string(cls) -> str:
        return f"{cls.MAJOR}.{cls.MINOR}.{cls.PATCH}"


def deprecated(since: str = "1.0.0", replacement: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator issuing deprecation warnings without breaking existing calls."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg = f"'{func.__name__}' has been deprecated since v{since}."
            if replacement:
                msg += f" Use '{replacement}' instead."
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            logger.warning(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class BackwardCompatLayer:
    """Adapter bridging legacy class parameter names or signatures to modern APIs."""

    @staticmethod
    def adapt_kwargs(kwargs: Dict[str, Any], remappings: Dict[str, str]) -> Dict[str, Any]:
        adapted = dict(kwargs)
        for old_key, new_key in remappings.items():
            if old_key in adapted:
                val = adapted.pop(old_key)
                adapted[new_key] = val
        return adapted


class SerializationCompat:
    """Maintains backward compatibility during .zk model deserialization across versions."""

    @staticmethod
    def migrate_header(header_dict: Dict[str, Any]) -> Dict[str, Any]:
        migrated = dict(header_dict)
        if "version" not in migrated:
            migrated["version"] = 1
        return migrated
