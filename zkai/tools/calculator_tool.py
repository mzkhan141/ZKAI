"""CalculatorTool for evaluating math expressions."""

from typing import Any
from zkai.tools.base import Tool, ToolMetadata, ToolResult


from zkai.core.logger import get_logger

logger = get_logger("tools.calculator")


import ast
import operator as op

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed in expressions")
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in operators:
            return operators[op_type](left, right)
        raise TypeError(f"Unsupported binary operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in operators:
            return operators[op_type](operand)
        raise TypeError(f"Unsupported unary operator: {op_type.__name__}")
    else:
        raise TypeError(f"Unsupported expression node: {type(node).__name__}")


class CalculatorTool(Tool):
    """Tool evaluating mathematical expressions cleanly and safely."""

    def __init__(self):
        meta = ToolMetadata(name="calculator", description="Evaluates mathematical expressions", category="utility")
        super().__init__(meta)

    def execute(self, expression: str, **kwargs: Any) -> ToolResult:
        try:
            tree = ast.parse(expression.strip(), mode="eval")
            val = safe_eval(tree.body)
            return ToolResult(tool_name=self.metadata.name, success=True, result=val)
        except Exception as e:
            logger.error(f"CalculatorTool execution failed for '{expression}': {e}")
            return ToolResult(tool_name=self.metadata.name, success=False, result=None, error=str(e))
