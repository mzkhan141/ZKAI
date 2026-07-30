"""Enhanced PluginSandbox for security isolation."""

import ast
from pathlib import Path
from typing import List
from zkai.core.exceptions import PluginError

BLOCKED_IMPORTS = {"os.system", "subprocess.Popen", "shutil.rmtree", "ctypes"}


class PluginSecuritySandbox:
    """Validates python codeAST for malicious or unsafe operations."""

    @staticmethod
    def validate_code(code_str: str) -> bool:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in BLOCKED_IMPORTS:
                        raise PluginError(f"Blocked import in plugin sandbox: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module in BLOCKED_IMPORTS:
                    raise PluginError(f"Blocked import from in plugin sandbox: {node.module}")
        return True

    @staticmethod
    def validate_file(file_path: str) -> bool:
        content = Path(file_path).read_text(encoding="utf-8")
        return PluginSecuritySandbox.validate_code(content)
