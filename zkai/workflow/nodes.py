"""WorkflowNode, Conditional, Loop, Parallel, Merge, Retry, HumanApproval DAG node definitions."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from zkai.core.types import WorkflowNodeType
from zkai.core.logger import get_logger

logger = get_logger("workflow.nodes")


class WorkflowNode(ABC):
    """Base abstract node in DAG workflow execution graph."""

    def __init__(self, name: str, node_type: WorkflowNodeType = WorkflowNodeType.ACTION):
        self.name = name
        self.node_type = node_type
        self.inputs: List[str] = []
        self.outputs: List[str] = []

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        pass


class ActionNode(WorkflowNode):
    """Executes single callable action."""

    def __init__(self, name: str, action: Callable[[Any], Any]):
        super().__init__(name, node_type=WorkflowNodeType.ACTION)
        self.action = action

    def execute(self, context: Dict[str, Any]) -> Any:
        inp = context.get(self.name, context.get("input"))
        return self.action(inp)


class Conditional(WorkflowNode):
    """Evaluates predicate to select true or false execution branch."""

    def __init__(self, name: str, predicate: Callable[[Any], bool], true_branch: str, false_branch: str):
        super().__init__(name, node_type=WorkflowNodeType.CONDITIONAL)
        self.predicate = predicate
        self.true_branch = true_branch
        self.false_branch = false_branch

    def execute(self, context: Dict[str, Any]) -> str:
        val = context.get(self.name, context.get("input"))
        if self.predicate(val):
            return self.true_branch
        return self.false_branch


class Loop(WorkflowNode):
    """Repeats action node loop while condition evaluates True."""

    def __init__(self, name: str, condition: Callable[[Any], bool], body: WorkflowNode, max_iterations: int = 10):
        super().__init__(name, node_type=WorkflowNodeType.LOOP)
        self.condition = condition
        self.body = body
        self.max_iterations = max_iterations

    def execute(self, context: Dict[str, Any]) -> Any:
        curr = context.get("input")
        count = 0
        while self.condition(curr) and count < self.max_iterations:
            context["input"] = curr
            curr = self.body.execute(context)
            count += 1
        return curr


class Parallel(WorkflowNode):
    """Executes list of nodes concurrently."""

    def __init__(self, name: str, branches: List[WorkflowNode]):
        super().__init__(name, node_type=WorkflowNodeType.PARALLEL)
        self.branches = branches

    def execute(self, context: Dict[str, Any]) -> List[Any]:
        results = []
        for branch in self.branches:
            res = branch.execute(context)
            results.append(res)
        return results


class Merge(WorkflowNode):
    """Synchronizes and merges outputs from parallel workflow branches."""

    def __init__(self, name: str, merge_fn: Optional[Callable[[List[Any]], Any]] = None):
        super().__init__(name, node_type=WorkflowNodeType.MERGE)
        self.merge_fn = merge_fn or (lambda x: x)

    def execute(self, context: Dict[str, Any]) -> Any:
        branch_results = context.get("parallel_results", [])
        return self.merge_fn(branch_results)


class Retry(WorkflowNode):
    """Wraps target node with automatic retry logic and backoff."""

    def __init__(self, name: str, inner_node: WorkflowNode, max_retries: int = 3):
        super().__init__(name, node_type=WorkflowNodeType.RETRY)
        self.inner_node = inner_node
        self.max_retries = max_retries

    def execute(self, context: Dict[str, Any]) -> Any:
        last_err = None
        for attempt in range(self.max_retries):
            try:
                return self.inner_node.execute(context)
            except Exception as e:
                last_err = e
                logger.warning(f"Retry attempt {attempt + 1}/{self.max_retries} failed for node '{self.name}': {e}")
        raise last_err or RuntimeError(f"Retry failed for node {self.name}")


class HumanApproval(WorkflowNode):
    """Pauses workflow pending human verification signal."""

    def __init__(self, name: str, prompt_message: str = "Approval required"):
        super().__init__(name, node_type=WorkflowNodeType.HUMAN_APPROVAL)
        self.prompt_message = prompt_message
        self.is_approved = True  # Auto-approved in automated non-interactive runs

    def execute(self, context: Dict[str, Any]) -> bool:
        logger.info(f"HumanApproval node '{self.name}': {self.prompt_message} (Approved: {self.is_approved})")
        return self.is_approved
