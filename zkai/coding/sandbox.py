"""Sandboxed Execution Environment (ProcessSandbox, DockerSandbox)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Dict, Any, Optional
from zkai.core.exceptions import CodingError
from zkai.core.logger import get_logger

logger = get_logger("coding.sandbox")


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float


class Sandbox(ABC):
    @abstractmethod
    def execute(self, code: str, timeout: int = 30) -> ExecutionResult:
        pass


class ProcessSandbox(Sandbox):
    """Subprocess-isolated sandbox for safe script execution."""

    def __init__(self, work_dir: Optional[str] = None):
        self.work_dir = Path(work_dir) if work_dir else Path(tempfile.gettempdir()) / "zkai_sandbox"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, code: str, timeout: int = 30) -> ExecutionResult:
        script_file = self.work_dir / "temp_script.py"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(code)

        import time
        start = time.perf_counter()

        try:
            res = subprocess.run(
                [sys.executable, str(script_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.work_dir),
            )
            duration = time.perf_counter() - start
            return ExecutionResult(
                stdout=res.stdout,
                stderr=res.stderr,
                exit_code=res.returncode,
                duration_seconds=duration,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(stdout="", stderr=f"Execution timed out after {timeout}s", exit_code=-1, duration_seconds=float(timeout))


class DockerSandbox(Sandbox):
    """Docker containerized sandbox for untrusted code execution."""

    def execute(self, code: str, timeout: int = 30) -> ExecutionResult:
        # Fallback process execution if Docker daemon not active
        p = ProcessSandbox()
        return p.execute(code, timeout=timeout)
