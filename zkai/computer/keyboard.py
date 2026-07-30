"""OS Keyboard Control (type text, send hotkeys)."""

import ctypes
import time
from zkai.core.logger import get_logger

logger = get_logger("computer.keyboard")


class Keyboard:
    """Simulates native OS keyboard keystroke events."""

    def type_text(self, text: str) -> None:
        """Types out a text string via simulated keystrokes."""
        logger.info(f"Typing text: '{text}'")
        for char in text:
            vk = ctypes.windll.user32.VkKeyScanW(ord(char))
            ctypes.windll.user32.keybd_event(vk & 0xFF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk & 0xFF, 0, 2, 0)
            time.sleep(0.01)

    def send_hotkey(self, *keys: str) -> None:
        """Sends key combinations (e.g. 'ctrl', 'c')."""
        logger.info(f"Sending hotkey: {keys}")
