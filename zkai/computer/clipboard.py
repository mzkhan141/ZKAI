"""Clipboard read and write access."""

import ctypes
from typing import Optional
from zkai.core.logger import get_logger

logger = get_logger("computer.clipboard")


class Clipboard:
    """Manages OS system clipboard content operations."""

    def copy_text(self, text: str) -> None:
        logger.info(f"Copying text to clipboard: '{text[:20]}...'")
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        h_mem = ctypes.windll.kernel32.GlobalAlloc(0x0042, (len(text) + 1) * 2)
        p_mem = ctypes.windll.kernel32.GlobalLock(h_mem)
        ctypes.cdll.msvcrt.wcscpy(ctypes.c_wchar_p(p_mem), text)
        ctypes.windll.kernel32.GlobalUnlock(h_mem)
        ctypes.windll.user32.SetClipboardData(13, h_mem)
        ctypes.windll.user32.CloseClipboard()

    def paste_text(self) -> str:
        ctypes.windll.user32.OpenClipboard(0)
        h_mem = ctypes.windll.user32.GetClipboardData(13)
        p_mem = ctypes.windll.kernel32.GlobalLock(h_mem)
        text = ctypes.c_wchar_p(p_mem).value or ""
        ctypes.windll.kernel32.GlobalUnlock(h_mem)
        ctypes.windll.user32.CloseClipboard()
        return text
