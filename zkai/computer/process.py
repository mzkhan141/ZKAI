"""ProcessManager and ApplicationLauncher for launching desktop applications."""

import subprocess
from pathlib import Path
from zkai.core.logger import get_logger

logger = get_logger("computer.process")


import shlex

class ApplicationLauncher:
    """Launches OS desktop applications by executable name or path safely."""

    @staticmethod
    def launch(app_name_or_path: str) -> bool:
        logger.info(f"Launching application: {app_name_or_path}")
        try:
            args = shlex.split(app_name_or_path)
            subprocess.Popen(args, shell=False)
            return True
        except Exception as e:
            logger.error(f"Failed to launch application '{app_name_or_path}': {e}")
            return False


class ProcessManager:
    """Manages active system processes safely."""

    def kill_process(self, process_name: str) -> None:
        logger.info(f"Killing process: {process_name}")
        try:
            clean_name = shlex.quote(process_name)
            subprocess.run(["taskkill", "/f", "/im", clean_name], shell=False, capture_output=True)
        except Exception as e:
            logger.error(f"Failed to kill process '{process_name}': {e}")
