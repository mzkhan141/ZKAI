"""AI Shell Package for ZKAI AI Operating System."""

from zkai.shell.cli import ArgparseCLIEngine, ClickCLIEngine, ZKAICLI, main
from zkai.shell.commands import Command, CommandRegistry
from zkai.shell.shell import ZKShell

__all__ = [
    "Command",
    "CommandRegistry",
    "ZKShell",
    "ZKAICLI",
    "ArgparseCLIEngine",
    "ClickCLIEngine",
    "main",
]
