"""KnowledgeGraph representing entities and relationships as graph nodes and edges."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType


@dataclass
class Node:
    id: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0


class KnowledgeGraph(BaseMemory):
    """Knowledge Graph memory allowing relational graph queries and traversal."""

    def __init__(self):
        super().__init__(MemoryType.KNOWLEDGE_GRAPH)
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node_id: str, label: str, properties: Optional[Dict[str, Any]] = None) -> Node:
        node = Node(id=node_id, label=label, properties=properties or {})
        self.nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, target_id: str, relation: str, weight: float = 1.0) -> Edge:
        edge = Edge(source_id=source_id, target_id=target_id, relation=relation, weight=weight)
        self.edges.append(edge)
        return edge

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        # Auto-create node for stored entry
        self.add_node(key, label=str(content))
        return MemoryEntry(key=key, content=content, memory_type=self.memory_type)

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        matching_nodes = [node for node in self.nodes.values() if query.lower() in node.id.lower() or query.lower() in node.label.lower()]
        return [MemoryEntry(key=node.id, content=node.label, memory_type=self.memory_type) for node in matching_nodes[:top_k]]

    def traverse(self, start_node_id: str, max_depth: int = 2) -> List[Node]:
        """Breadth-first traversal from start node."""
        visited = set()
        queue = [(start_node_id, 0)]
        result = []

        while queue:
            curr_id, depth = queue.pop(0)
            if curr_id in visited or depth > max_depth:
                continue
            visited.add(curr_id)
            if curr_id in self.nodes:
                result.append(self.nodes[curr_id])

            for edge in self.edges:
                if edge.source_id == curr_id and edge.target_id not in visited:
                    queue.append((edge.target_id, depth + 1))

        return result

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()
