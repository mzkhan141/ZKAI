"""SandboxPolicies for code execution restriction."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class SandboxPolicy:
    allow_network: bool = False
    allow_file_write: bool = False
    allowed_imports: List[str] = field(default_factory=lambda: ["math", "random", "time", "json", "re"])
    max_memory_mb: int = 512
    max_execution_time_sec: int = 30
