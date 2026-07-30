"""HotReloader for tracking plugin file changes and reloading plugins dynamically."""

from pathlib import Path
import time
from typing import Callable, Dict
from zkai.core.logger import get_logger

logger = get_logger("plugins.hot_reload")


class HotReloader:
    """Monitors plugin file modification timestamps and triggers reload callback."""

    def __init__(self, watch_dir: str, reload_callback: Callable[[str], None]):
        self.watch_dir = Path(watch_dir)
        self.reload_callback = reload_callback
        self.file_mtimes: Dict[str, float] = {}
        self._update_mtimes()

    def _update_mtimes(self) -> None:
        if not self.watch_dir.exists():
            return
        for p in self.watch_dir.rglob("*.py"):
            self.file_mtimes[str(p)] = p.stat().st_mtime

    def check_for_changes(self) -> bool:
        changed = False
        if not self.watch_dir.exists():
            return False
        for p in self.watch_dir.rglob("*.py"):
            mtime = p.stat().st_mtime
            str_p = str(p)
            if str_p not in self.file_mtimes or self.file_mtimes[str_p] < mtime:
                logger.info(f"File change detected in plugin: {p.name}")
                self.file_mtimes[str_p] = mtime
                changed = True
                self.reload_callback(str_p)
        return changed
