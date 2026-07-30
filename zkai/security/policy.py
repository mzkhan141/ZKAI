"""Policy Engine for declarative rule enforcement."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass
class Policy:
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    action: str = "allow"


class PolicyEngine:
    """Evaluates declarative policies against context payloads."""

    def __init__(self):
        self.policies: List[Policy] = []

    def add_policy(self, policy: Policy) -> None:
        self.policies.append(policy)

    def evaluate(self, context: Dict[str, Any]) -> bool:
        for policy in self.policies:
            if policy.condition(context):
                if policy.action == "deny":
                    return False
        return True
