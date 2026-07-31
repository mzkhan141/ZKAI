"""Plugin Manifest specification and loader."""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from zkai.core.exceptions import PluginError


@dataclass
class PluginManifest:
    name: str
    version: str
    description: str
    author: str
    entry_point: str = "plugin.py"
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: str) -> "PluginManifest":
        p = Path(path)
        if not p.exists():
            raise PluginError(f"Manifest file not found: {path}")
        content = p.read_text(encoding="utf-8")
        if p.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(content)
        else:
            data = json.loads(content)
        return cls(**data)
