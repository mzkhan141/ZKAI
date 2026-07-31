"""AgentExecutor executing action plans."""

from dataclasses import dataclass, field
from typing import Any, List, Dict
from zkai.agent.plan import Plan, Action
from zkai.tools.base import ToolRegistry
from zkai.core.logger import get_logger

logger = get_logger("agent.executor")


@dataclass
class ActionHistory:
    action: Action
    result: Any
    success: bool


class AgentExecutor:
    """Executes planned actions using registered tool plugins."""

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.history: List[ActionHistory] = []

    def execute_plan(self, plan: Plan) -> List[ActionHistory]:
        logger.info(f"Executing plan with {len(plan.actions)} actions...")
        for act in plan.actions:
            tool = self.tool_registry.get(act.tool_name)
            if tool:
                res = tool(**act.arguments)
                hist = ActionHistory(action=act, result=res.result, success=res.success)
                self.history.append(hist)
            else:
                logger.error(f"Tool {act.tool_name} not found in registry.")
        return self.history
