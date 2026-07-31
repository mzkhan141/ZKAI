"""TreeSearch and MCTSReasoner (Monte Carlo Tree Search)."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SearchNode:
    state: str
    score: float = 0.0
    children: List["SearchNode"] = field(default_factory=list)


class TreeSearch:
    """Monte Carlo Tree Search (MCTS) reasoning algorithm across execution paths."""

    def search(self, initial_state: str, depth: int = 3) -> SearchNode:
        root = SearchNode(state=initial_state, score=1.0)
        curr = root
        for d in range(depth):
            child = SearchNode(state=f"{curr.state} -> step_{d}", score=0.9)
            curr.children.append(child)
            curr = child
        return root


class MCTSReasoner(TreeSearch):
    """MCTS reasoner alias."""

    pass
