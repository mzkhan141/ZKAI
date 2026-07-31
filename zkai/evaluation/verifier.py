"""Verifier checking strict constraints, assertions, and outputs."""

from dataclasses import dataclass
from typing import Any, Callable, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("evaluation.verifier")


@dataclass
class VerificationResult:
    """Output from constraint verification."""
    passed: bool
    violations: List[str]


class Verifier:
    """Verifies that generated responses comply with formal rules and constraints."""

    def __init__(self):
        self.rules: List[Callable[[str], bool]] = []

    def add_rule(self, rule_fn: Callable[[str], bool]) -> None:
        self.rules.append(rule_fn)

    def verify(self, response: str) -> VerificationResult:
        violations = []
        for idx, rule in enumerate(self.rules):
            try:
                if not rule(response):
                    violations.append(f"Rule #{idx+1} failed verification.")
            except Exception as e:
                violations.append(f"Rule #{idx+1} raised error: {e}")

        return VerificationResult(passed=(len(violations) == 0), violations=violations)
