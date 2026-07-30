"""ProjectGenerator for scaffolding directory trees and boilerplate files."""

from pathlib import Path
from typing import Dict
from zkai.core.logger import get_logger

logger = get_logger("coding.project")


class ProjectGenerator:
    """Scaffolds complete multi-file software project structures on disk."""

    def create_project(self, root_dir: str, file_map: Dict[str, str]) -> str:
        base = Path(root_dir)
        base.mkdir(parents=True, exist_ok=True)

        for rel_path, content in file_map.items():
            full_path = base / rel_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        logger.info(f"Generated software project with {len(file_map)} files at {root_dir}")
        return str(base)
