"""OS Mouse Control (move, click, drag, scroll) using ctypes win32 API."""

from typing import Optional
import ctypes
import time
from zkai.core.logger import get_logger

logger = get_logger("computer.mouse")

# Windows API constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800


class Mouse:
    """Simulates native OS mouse input events."""

    def move(self, x: int, y: int) -> None:
        """Moves mouse cursor to target screen coordinates (x, y)."""
        logger.info(f"Mouse move to ({x}, {y})")
        ctypes.windll.user32.SetCursorPos(x, y)

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left") -> None:
        """Clicks mouse button at coordinates."""
        if x is not None and y is not None:
            self.move(x, y)
        time.sleep(0.05)
        if button == "left":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif button == "right":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        logger.info(f"Mouse {button} click executed at ({x}, {y})")

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        self.move(start_x, start_y)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        self.move(end_x, end_y)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def scroll(self, clicks: int) -> None:
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, clicks * 120, 0)
