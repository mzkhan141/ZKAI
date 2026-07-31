"""Virtual Environment Manager and Package Installer."""

import subprocess
import venv
from pathlib import Path
from zkai.core.logger import get_logger

logger = get_logger("coding.venv")


class VirtualEnvManager:
    """Manages virtual environment creation and pip package installation."""

    def __init__(self, venv_dir: str = "./zkai_env"):
        self.venv_dir = Path(venv_dir)

    def create(self) -> str:
        if not self.venv_dir.exists():
            logger.info(f"Creating python virtualenv at {self.venv_dir}")
            venv.create(self.venv_dir, with_pip=True)
        return str(self.venv_dir)

    def install(self, package_name: str) -> bool:
        python_bin = self.venv_dir / "Scripts" / "python.exe" if self.venv_dir.joinpath("Scripts").exists() else self.venv_dir / "bin" / "python"
        res = subprocess.run([str(python_bin), "-m", "pip", "install", package_name], capture_output=True, text=True)
        return res.returncode == 0
