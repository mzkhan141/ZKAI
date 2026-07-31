"""CompilerWrapper for compiling C/C++/Rust source files."""

import subprocess
from pathlib import Path
from zkai.core.logger import get_logger

logger = get_logger("coding.compiler")


class CompilerWrapper:
    """Wrapper invoking system compilers (gcc, g++, rustc) for native code."""

    def compile_cpp(self, source_path: str, output_path: str) -> bool:
        logger.info(f"Compiling C++ file {source_path} -> {output_path}")
        res = subprocess.run(["g++", "-O3", source_path, "-o", output_path], capture_output=True, text=True)
        return res.returncode == 0
