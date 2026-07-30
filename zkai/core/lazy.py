"""LazyModule and LazyImport for deferred module loading and fast startup."""

import importlib
from typing import Any, Callable, Optional
from zkai.core.logger import get_logger

logger = get_logger("core.lazy")


class LazyImport:
    """Defers heavy third-party package imports until first attribute access."""

    def __init__(self, module_name: str):
        self._module_name = module_name
        self._module: Optional[Any] = None

    def _load(self) -> Any:
        if self._module is None:
            self._module = importlib.import_module(self._module_name)
        return self._module

    def __getattr__(self, name: str) -> Any:
        mod = self._load()
        return getattr(mod, name)


class LazyModule:
    """Defers neural module weights initialization until first forward invocation."""

    def __init__(self, factory_fn: Callable[[], Any]):
        self._factory_fn = factory_fn
        self._instance: Optional[Any] = None

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._instance is None:
            logger.debug("Executing deferred LazyModule initialization...")
            self._instance = self._factory_fn()
        return self._instance(*args, **kwargs)
