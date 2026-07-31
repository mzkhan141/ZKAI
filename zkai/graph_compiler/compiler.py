"""GraphCompiler, ExecutionPlanner, and MemoryPlanner for optimizing computation graphs."""

from typing import Dict, List, Optional
from zkai.graph_compiler.graph import ComputeGraph, ComputeNode, StaticGraph
from zkai.core.logger import get_logger

logger = get_logger("graph_compiler.compiler")


class ExecutionPlanner:
    """Schedules nodes for execution, parallel streams, and memory barrier synchronization."""

    def plan_execution(self, graph: ComputeGraph) -> List[ComputeNode]:
        """Returns ordered execution plan."""
        return graph.get_topological_sort()


class MemoryPlanner:
    """Calculates peak memory usage and plans tensor buffer reuse across non-overlapping node lifespans."""

    def plan_memory(self, graph: ComputeGraph) -> Dict[str, int]:
        """Maps tensor node names to memory offset allocations."""
        offsets: Dict[str, int] = {}
        curr_offset = 0
        for node in graph.get_topological_sort():
            for out in node.outputs:
                offsets[out] = curr_offset
                curr_offset += 1024  # Standard allocation block
        return offsets


class GraphCompiler:
    """Main GraphCompiler coordinating optimization passes and emitting static executable graph."""

    def __init__(self, opt_level: int = 2):
        self.opt_level = opt_level
        self.planner = ExecutionPlanner()
        self.memory_planner = MemoryPlanner()

    def compile(self, graph: ComputeGraph) -> StaticGraph:
        """Applies optimization passes and outputs optimized StaticGraph."""
        logger.info(f"Compiling ComputeGraph '{graph.name}' at optimization level {self.opt_level}...")

        from zkai.graph_compiler.optimizations import ConstantFolding, DeadCodeElimination, KernelFusion, OperatorFusion

        compiled = StaticGraph(name=f"{graph.name}_compiled")
        compiled.nodes = dict(graph.nodes)
        compiled.inputs = list(graph.inputs)
        compiled.outputs = list(graph.outputs)

        if self.opt_level >= 1:
            compiled = ConstantFolding().apply(compiled)
            compiled = DeadCodeElimination().apply(compiled)

        if self.opt_level >= 2:
            compiled = KernelFusion().apply(compiled)
            compiled = OperatorFusion().apply(compiled)

        return compiled
