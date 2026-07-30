"""Computer Interaction, OS Automation, Mouse/Keyboard, UI Detection, and Screen OCR for ZKAI."""

from zkai.computer.mouse import Mouse
from zkai.computer.keyboard import Keyboard
from zkai.computer.monitor import Monitor, ScreenCapture
from zkai.computer.window import Window, WindowDetector
from zkai.computer.clipboard import Clipboard
from zkai.computer.ui_detection import UIElementDetector, TemplateMatching, UIElement
from zkai.computer.automation import Automation, ActionSequence, Action
from zkai.computer.ocr import ComputerOCR
from zkai.computer.process import ApplicationLauncher, ProcessManager
from zkai.computer.file_explorer import FileExplorer

__all__ = [
    "Mouse",
    "Keyboard",
    "Monitor",
    "ScreenCapture",
    "Window",
    "WindowDetector",
    "Clipboard",
    "UIElementDetector",
    "TemplateMatching",
    "UIElement",
    "Automation",
    "ActionSequence",
    "Action",
    "ComputerOCR",
    "ApplicationLauncher",
    "ProcessManager",
    "FileExplorer",
]
