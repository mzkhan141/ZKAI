"""AgentReflection and AgentCritic."""

from zkai.core.logger import get_logger

logger = get_logger("agent.reflection")


class AgentCritic:
    """Evaluates agent execution results for failures."""

    def evaluate_execution(self, success: bool, output: str) -> str:
        if not success:
            return f"Execution failed: {output}. Action retry recommended."
        return "Execution succeeded."


class AgentReflection:
    """Reflects on tool execution outcomes to refine strategy."""

    def reflect_on_failure(self, error_message: str) -> str:
        logger.info(f"Agent self-reflecting on error: {error_message}")
        return "Adjust tool selection parameters and retry."
