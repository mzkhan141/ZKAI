"""AgentNegotiation and ConsensusProtocol."""

from typing import List


class ConsensusProtocol:
    """Computes majority consensus across multi-agent proposals."""

    @staticmethod
    def compute_consensus(proposals: List[str]) -> str:
        if not proposals:
            return ""
        from collections import Counter
        counts = Counter(proposals)
        return counts.most_common(1)[0][0]
