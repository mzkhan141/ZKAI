"""WorkflowEngine and WorkflowRunner for building and executing complex DAG workflows."""

from typing import Any, Dict, List, Optional
from zkai.workflow.nodes import ActionNode, WorkflowNode
from zkai.core.logger import get_logger

logger = get_logger("workflow.engine")


class WorkflowEngine:
    """DAG Workflow builder constructing interconnected execution steps."""

    def __init__(self, name: str = "main_workflow"):
        self.name = name
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = {}

    def add_node(self, node: WorkflowNode) -> "WorkflowEngine":
        self.nodes[node.name] = node
        if node.name not in self.edges:
            self.edges[node.name] = []
        return self

    def add_edge(self, from_node: str, to_node: str) -> "WorkflowEngine":
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
        return self


class WorkflowRunner:
    """Runs a DAG workflow to completion maintaining execution context."""

    def __init__(self, engine: WorkflowEngine):
        self.engine = engine

    def run(self, initial_input: Any = None) -> Any:
        logger.info(f"Running DAG workflow '{self.engine.name}' with {len(self.engine.nodes)} nodes...")
        context: Dict[str, Any] = {"input": initial_input}
        current_input = initial_input

        for node_name, node in self.engine.nodes.items():
            context["input"] = current_input
            res = node.execute(context)
            context[node_name] = res
            current_input = res

        return current_input
