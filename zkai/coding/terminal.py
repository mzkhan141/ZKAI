"""Terminal and shell command execution session."""

from typing import Optional
import subprocess
from zkai.core.logger import get_logger

logger = get_logger("coding.terminal")


class TerminalSession:
    """Session managing terminal command execution."""

    def run_command(self, command: str, cwd: Optional[str] = None) -> str:
        logger.info(f"Running terminal command: '{command}'")
        res = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        if res.returncode != 0:
            return f"Command Error ({res.returncode}):\n{res.stderr}"
        return res.stdout


class Terminal:
    """Terminal wrapper interface."""

    def __init__(self):
        self.session = TerminalSession()

    def execute(self, cmd: str) -> str:
        return self.session.run_command(cmd)
