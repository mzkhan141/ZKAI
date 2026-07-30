"""Dual-engine CLI entry point for 'zk' command line utility."""

import argparse
import sys
from typing import List, Optional
from zkai.shell.shell import ZKShell
from zkai.core.logger import get_logger

logger = get_logger("shell.cli")

try:
    import click
except ImportError:
    click = None


class ArgparseCLIEngine:
    """Zero-dependency argparse-based CLI engine."""

    def __init__(self, shell: ZKShell):
        self.shell = shell

    def run(self, args: Optional[List[str]] = None) -> str:
        parser = argparse.ArgumentParser(prog="zk", description="ZKAI AI Operating System Command Line Interface")
        parser.add_argument("command", nargs="?", default="shell", help="Command to execute")
        parser.add_argument("cmd_args", nargs="*", help="Arguments for the command")
        parser.add_argument("--engine", choices=["argparse", "click"], default="argparse", help="CLI parser engine")

        parsed = parser.parse_args(args or sys.argv[1:])
        full_line = f"{parsed.command} {' '.join(parsed.cmd_args)}".strip()
        return self.shell.execute_line(full_line)


class ClickCLIEngine:
    """Rich click-based CLI engine."""

    def __init__(self, shell: ZKShell):
        self.shell = shell

    def run(self, args: Optional[List[str]] = None) -> str:
        if not click:
            logger.warning("Click library not installed, falling back to argparse engine.")
            return ArgparseCLIEngine(self.shell).run(args)

        @click.group()
        def cli():
            """ZKAI AI Operating System CLI"""
            pass

        @cli.command()
        @click.argument("prompt", nargs=-1)
        def chat(prompt):
            click.echo(self.shell.execute_line(f"chat {' '.join(prompt)}"))

        # Fallback runner
        full_line = " ".join(args) if args else "shell"
        return self.shell.execute_line(full_line)


class ZKAICLI:
    """Master CLI delegating to chosen engine (argparse or click)."""

    def __init__(self, preferred_engine: str = "argparse"):
        self.shell = ZKShell()
        self.preferred_engine = preferred_engine
        self.argparse_engine = ArgparseCLIEngine(self.shell)
        self.click_engine = ClickCLIEngine(self.shell)

    def main(self, args: Optional[List[str]] = None) -> str:
        if self.preferred_engine == "click" and click:
            return self.click_engine.run(args)
        return self.argparse_engine.run(args)


def main():
    cli = ZKAICLI()
    out = cli.main()
    if out:
        print(out)


if __name__ == "__main__":
    main()
