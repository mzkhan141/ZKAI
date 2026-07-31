"""APIDocGenerator producing markdown API reference documentation."""

import inspect
from typing import Any


class APIDocGenerator:
    """Generates markdown documentation for Python classes and modules."""

    def generate_class_doc(self, cls: type) -> str:
        lines = [f"# Class `{cls.__name__}`", "", cls.__doc__ or "No docstring provided.", ""]
        lines.append("## Methods")
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not name.startswith("_"):
                sig = inspect.signature(method)
                doc = method.__doc__ or ""
                lines.append(f"### `{name}{sig}`")
                lines.append(f"{doc}\n")
        return "\n".join(lines)
