"""Code Profiler using cProfile."""

import cProfile
import pstats
import io
from zkai.core.logger import get_logger

logger = get_logger("coding.profiler")


import os
import subprocess
import sys
import tempfile


class CodeProfiler:
    """Profiles Python code execution bottlenecks in an isolated process."""

    def profile_code(self, code_str: str) -> str:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
            tf.write(code_str)
            temp_path = tf.name

        try:
            res = subprocess.run(
                [sys.executable, "-m", "cProfile", "-s", "cumulative", temp_path],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            return res.stdout if res.returncode == 0 else res.stderr
        except Exception as e:
            logger.error(f"Code profiling failed: {e}")
            return f"Profiling error: {e}"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
