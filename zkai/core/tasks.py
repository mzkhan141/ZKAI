"""Production Task Scheduler, Priority Queue, and Parallel Executors for ZKAI."""

import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
import heapq
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
import uuid

from zkai.core.types import Priority, TaskStatus
from zkai.core.exceptions import ZKAIError
from zkai.core.logger import get_logger

logger = get_logger("tasks")

T = TypeVar("T")


class CancellationToken:
    """Token used to signal task cancellation across threads and coroutines."""

    def __init__(self):
        self._is_cancelled = False

    def cancel(self) -> None:
        self._is_cancelled = True

    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled

    def raise_if_cancelled(self) -> None:
        if self._is_cancelled:
            raise ZKAIError("Operation was cancelled via CancellationToken")


@dataclass
class RetryPolicy:
    """Configures automatic retry behavior for tasks."""
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay: float = 1.0


@dataclass
class TimeoutPolicy:
    """Configures execution timeout limits."""
    timeout_seconds: Optional[float] = 30.0


@dataclass(order=True)
class Task(Generic[T]):
    """Represents a scheduled unit of work."""
    priority: int = field(init=True)
    created_at: float = field(init=False, default_factory=time.time)
    task_id: str = field(init=False, default_factory=lambda: str(uuid.uuid4()))
    func: Callable[..., T] = field(compare=False)
    args: tuple = field(default=(), compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)
    result: Optional[T] = field(default=None, compare=False)
    error: Optional[Exception] = field(default=None, compare=False)
    retry_policy: Optional[RetryPolicy] = field(default=None, compare=False)
    timeout_policy: Optional[TimeoutPolicy] = field(default=None, compare=False)

    def __post_init__(self):
        # Reverse priority so higher int comes first in heap
        self.priority = -int(self.priority)


class PriorityQueue(Generic[T]):
    """Heap-based priority queue for tasks."""

    def __init__(self):
        self._heap: List[Task[T]] = []

    def push(self, task: Task[T]) -> None:
        heapq.heappush(self._heap, task)

    def pop(self) -> Task[T]:
        return heapq.heappop(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)


class TaskQueue:
    """Asynchronous Queue wrapper for Task objects."""

    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()

    async def put(self, task: Task) -> None:
        await self._queue.put(task)

    async def get(self) -> Task:
        return await self._queue.get()

    def empty(self) -> bool:
        return self._queue.empty()


class BackgroundTask:
    """Handles async execution of a background Task."""

    def __init__(self, task: Task):
        self.task = task
        self._async_task: Optional[asyncio.Task] = None

    async def run(self) -> Any:
        self.task.status = TaskStatus.RUNNING
        retries = 0
        max_retries = self.task.retry_policy.max_retries if self.task.retry_policy else 0
        delay = self.task.retry_policy.initial_delay if self.task.retry_policy else 1.0

        while True:
            try:
                if self.task.timeout_policy and self.task.timeout_policy.timeout_seconds:
                    if asyncio.iscoroutinefunction(self.task.func):
                        res = await asyncio.wait_for(
                            self.task.func(*self.task.args, **self.task.kwargs),
                            timeout=self.task.timeout_policy.timeout_seconds,
                        )
                    else:
                        res = await asyncio.to_thread(self.task.func, *self.task.args, **self.task.kwargs)
                else:
                    if asyncio.iscoroutinefunction(self.task.func):
                        res = await self.task.func(*self.task.args, **self.task.kwargs)
                    else:
                        res = await asyncio.to_thread(self.task.func, *self.task.args, **self.task.kwargs)

                self.task.result = res
                self.task.status = TaskStatus.COMPLETED
                return res
            except Exception as e:
                retries += 1
                if retries <= max_retries:
                    self.task.status = TaskStatus.RETRYING
                    logger.warning(f"Task {self.task.task_id} failed. Retrying {retries}/{max_retries} in {delay}s...")
                    await asyncio.sleep(delay)
                    delay *= self.task.retry_policy.backoff_factor if self.task.retry_policy else 1.0
                else:
                    self.task.error = e
                    self.task.status = TaskStatus.FAILED
                    logger.error(f"Task {self.task.task_id} permanently failed: {e}")
                    raise e


class TaskExecutor:
    """Worker pool executor for tasks using thread pools."""

    def __init__(self, max_workers: int = 4):
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> asyncio.Future:
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(self._thread_pool, lambda: func(*args, **kwargs))

    def shutdown(self) -> None:
        self._thread_pool.shutdown(wait=True)


class ParallelExecutor:
    """Executes multiple functions concurrently using asyncio.gather or thread pool."""

    @staticmethod
    async def run_parallel(tasks: List[Callable[[], Any]]) -> List[Any]:
        async_tasks = [asyncio.to_thread(t) if not asyncio.iscoroutinefunction(t) else t() for t in tasks]
        return await asyncio.gather(*async_tasks)


class WorkflowExecutor:
    """Executes a chain/DAG of dependent tasks in order."""

    def __init__(self):
        self.steps: List[Callable[[Any], Any]] = []

    def add_step(self, func: Callable[[Any], Any]) -> "WorkflowExecutor":
        self.steps.append(func)
        return self

    async def execute(self, initial_input: Any) -> Any:
        current = initial_input
        for step in self.steps:
            if asyncio.iscoroutinefunction(step):
                current = await step(current)
            else:
                current = await asyncio.to_thread(step, current)
        return current
