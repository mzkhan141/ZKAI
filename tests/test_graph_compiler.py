"""Tests for GraphCompiler, ComputeGraph, and optimization passes."""

import pytest
from zkai.graph_compiler.graph import ComputeGraph, ComputeNode, DynamicGraph, StaticGraph
from zkai.graph_compiler.compiler import GraphCompiler, ExecutionPlanner, MemoryPlanner
from zkai.graph_compiler.optimizations import ConstantFolding, DeadCodeElimination
from zkai.neural.tensor import Tensor


def test_compute_graph_topological_sort():
    g = ComputeGraph("test_g")
    n1 = ComputeNode(node_id="n1", op_type="input", outputs=["out1"])
    n2 = ComputeNode(node_id="n2", op_type="add", inputs=["out1"], outputs=["out2"])
    g.add_node(n1)
    g.add_node(n2)

    topo = g.get_topological_sort()
    assert len(topo) == 2
    assert topo[0].node_id == "n1"


def test_graph_compiler_optimizations():
    compiler = GraphCompiler(opt_level=2)
    g = ComputeGraph("test_g")
    n1 = ComputeNode(node_id="n1", op_type="placeholder", outputs=["out1"])
    g.add_node(n1)
    g.inputs.append("out1")
    g.outputs.append("out1")

    compiled = compiler.compile(g)
    assert isinstance(compiled, StaticGraph)


def test_dynamic_graph_tracing():
    dg = DynamicGraph("dynamic_test")
    sg = dg.trace(lambda x: x, Tensor([1.0]))
    assert isinstance(sg, StaticGraph)
    assert len(sg.nodes) >= 1
