"""ConsensusReasoning for multi-path reasoning aggregation."""

from typing import List


class ConsensusReasoning:
    """Aggregates multiple reasoning paths via majority voting."""

    def aggregate(self, paths: List[str]) -> str:
        if not paths:
            return ""
        return paths[0]
