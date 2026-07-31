"""WorkflowScheduler for cron-based and periodic execution of workflows."""

from typing import Any, Callable, Dict, List, Optional, Tuple
from zkai.workflow.engine import WorkflowRunner
from zkai.core.logger import get_logger

logger = get_logger("workflow.scheduler")


class WorkflowScheduler:
    """Schedules workflows for periodic, async, or cron-triggered execution."""

    def __init__(self):
        self.scheduled_runners: List[Tuple[WorkflowRunner, str]] = []

    def schedule(self, runner: WorkflowRunner, cron_expression: str = "*/5 * * * *") -> None:
        """Schedules runner for execution on given cron interval."""
        self.scheduled_runners.append((runner, cron_expression))
        logger.info(f"Scheduled workflow '{runner.engine.name}' with schedule '{cron_expression}'")

    def run_all_pending(self, initial_input: Any = None) -> List[Any]:
        """Runs all registered scheduled workflows once."""
        results = []
        for runner, cron in self.scheduled_runners:
            res = runner.run(initial_input)
            results.append(res)
        return results
