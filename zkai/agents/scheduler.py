"""TaskScheduler for distributing tasks across specialized agents."""

from typing import Any, Dict, List
from zkai.core.tasks import TaskQueue


class TaskScheduler:
    """Schedules and dispatches task queues across agent pools."""

    def __init__(self):
        self.queue = TaskQueue()

    def schedule_task(self, task_name: str, payload: Dict[str, Any]) -> None:
        self.queue.add_task(task_name, payload)
