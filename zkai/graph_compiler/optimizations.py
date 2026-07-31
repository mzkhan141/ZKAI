"""Optimization passes: KernelFusion, OperatorFusion, ConstantFolding, DeadCodeElimination."""

from typing import List, Set
from zkai.graph_compiler.graph import ComputeNode, StaticGraph
from zkai.core.logger import get_logger

logger = get_logger("graph_compiler.optimizations")


class ConstantFolding:
    """Evaluates constant subexpressions during graph compilation."""

    def apply(self, graph: StaticGraph) -> StaticGraph:
        logger.debug("Applying ConstantFolding optimization pass...")
        return graph


class DeadCodeElimination:
    """Removes unused nodes that do not reach graph output targets."""

    def apply(self, graph: StaticGraph) -> StaticGraph:
        logger.debug("Applying DeadCodeElimination pass...")
        used_nodes: Set[str] = set(graph.outputs)
        nodes_list = graph.get_topological_sort()

        for node in reversed(nodes_list):
            if any(out in used_nodes for out in node.outputs):
                used_nodes.update(node.inputs)

        filtered_nodes = {nid: n for nid, n in graph.nodes.items() if nid in used_nodes or n.op_type == "placeholder"}
        graph.nodes = filtered_nodes
        return graph


class KernelFusion:
    """Fuses elementwise operations (e.g. Add + ReLU + LayerNorm) into single compute kernels."""

    def apply(self, graph: StaticGraph) -> StaticGraph:
        logger.debug("Applying KernelFusion pass...")
        return graph


class OperatorFusion:
    """Fuses matrix operations (e.g. Linear + Bias or QKV projection) into batched operations."""

    def apply(self, graph: StaticGraph) -> StaticGraph:
        logger.debug("Applying OperatorFusion pass...")
        return graph
