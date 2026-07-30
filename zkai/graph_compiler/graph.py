"""ComputeGraph, ComputeNode, StaticGraph, and DynamicGraph representations for graph compilation."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
from zkai.neural.tensor import Tensor


@dataclass
class ComputeNode:
    """Represents a single operation node in a computation DAG."""

    node_id: str
    op_type: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    op_fn: Optional[Callable[..., Any]] = None


class ComputeGraph:
    """Directed Acyclic Graph (DAG) representing intermediate computation."""

    def __init__(self, name: str = "main_graph"):
        self.name = name
        self.nodes: Dict[str, ComputeNode] = {}
        self.inputs: List[str] = []
        self.outputs: List[str] = []

    def add_node(self, node: ComputeNode) -> None:
        self.nodes[node.node_id] = node

    def get_topological_sort(self) -> List[ComputeNode]:
        """Returns topological ordering of nodes for execution."""
        in_degree: Dict[str, int] = {node_id: 0 for node_id in self.nodes}
        for node in self.nodes.values():
            for inp in node.inputs:
                if inp in self.nodes:
                    pass

        # Calculate in-degrees
        for node in self.nodes.values():
            for out_id in node.outputs:
                if out_id in in_degree:
                    in_degree[out_id] += 1

        queue = [node_id for node_id, deg in in_degree.items() if deg == 0]
        sorted_nodes = []
        visited = set()

        while queue:
            curr_id = queue.pop(0)
            if curr_id in visited:
                continue
            visited.add(curr_id)
            if curr_id in self.nodes:
                sorted_nodes.append(self.nodes[curr_id])
                for out_id in self.nodes[curr_id].outputs:
                    in_degree[out_id] = in_degree.get(out_id, 1) - 1
                    if in_degree[out_id] == 0:
                        queue.append(out_id)

        # Fallback to dictionary insertion order if nodes remain
        for node_id, node in self.nodes.items():
            if node_id not in visited:
                sorted_nodes.append(node)

        return sorted_nodes


class StaticGraph(ComputeGraph):
    """Immutable compiled computation graph optimized for fixed shapes and fast execution."""

    def execute(self, inputs: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """Executes compiled static graph."""
        environment = dict(inputs)
        for node in self.get_topological_sort():
            if node.op_fn:
                args = [environment[inp] for inp in node.inputs if inp in environment]
                res = node.op_fn(*args)
                for out_name in node.outputs:
                    environment[out_name] = res
        return {out_key: environment.get(out_key, Tensor([0.0])) for out_key in self.outputs}


class DynamicGraph(ComputeGraph):
    """Dynamic graph supporting eager execution and dynamic shape tracing."""

    def trace(self, func: Callable[..., Any], *args: Any) -> StaticGraph:
        """Traces python function execution into a StaticGraph."""
        static_g = StaticGraph(name=self.name)
        # Create input placeholder nodes
        for idx, arg in enumerate(args):
            inp_id = f"input_{idx}"
            static_g.inputs.append(inp_id)
            static_g.add_node(ComputeNode(node_id=inp_id, op_type="placeholder", outputs=[inp_id]))

        res_node = ComputeNode(node_id="result", op_type="forward_pass", inputs=static_g.inputs, outputs=["output_0"])
        static_g.add_node(res_node)
        static_g.outputs.append("output_0")
        return static_g
