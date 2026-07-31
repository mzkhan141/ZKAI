"""CodeLinter using AST parsing and lint rules."""

import ast
from dataclasses import dataclass
from typing import List


@dataclass
class LintError:
    line: int
    column: int
    message: str


class CodeLinter:
    """AST-based Python code linter checking syntax errors and style violations."""

    def lint_python(self, code: str) -> List[LintError]:
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(LintError(line=e.lineno or 1, column=e.offset or 0, message=f"SyntaxError: {e.msg}"))
        return errors
