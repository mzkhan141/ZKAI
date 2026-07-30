"""PythonRunner for sandboxed code execution and output capture."""

from typing import Optional
from zkai.coding.sandbox import ProcessSandbox, ExecutionResult
from zkai.core.logger import get_logger

logger = get_logger("coding.runner")


class PythonRunner:
    """High-level Python code runner."""

    def __init__(self):
        self.sandbox = ProcessSandbox()

    def run(self, code: str, timeout: int = 30) -> ExecutionResult:
        """Runs Python code string safely in isolated sandbox."""
        logger.info("Executing Python code block...")
        return self.sandbox.execute(code, timeout=timeout)
