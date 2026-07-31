"""Static Analysis and AST inspection."""

import ast
from typing import Dict, List, Any


class StaticAnalyzer:
    """Analyzes AST tree structure, function definitions, and dependencies."""

    def analyze(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
            return {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "valid_syntax": True,
            }
        except SyntaxError as e:
            return {"valid_syntax": False, "error": str(e)}
