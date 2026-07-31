"""Window and WindowDetector for active OS application window management."""

import ctypes
from dataclasses import dataclass
from typing import List, Optional
from zkai.core.logger import get_logger

logger = get_logger("computer.window")


@dataclass
class Window:
    handle: int
    title: str


class WindowDetector:
    """Detects and enumerates open OS application windows."""

    def get_active_window(self) -> Window:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        return Window(handle=hwnd, title=buff.value)
