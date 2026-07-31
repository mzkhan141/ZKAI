"""Domain-specific schedulers for the ZKAI AI Kernel."""

import asyncio
from typing import Any, Dict, List, Optional
from zkai.core.tasks import Task, PriorityQueue, TaskExecutor
from zkai.core.types import Priority
from zkai.core.logger import get_logger
from zkai.kernel.types import ResourceType, SchedulerPolicy

logger = get_logger("kernel.scheduler")


class PriorityScheduler:
    """Heap-based pre-emptive priority scheduler wrapping PriorityQueue."""

    def __init__(self):
        self._queue: PriorityQueue[Task] = PriorityQueue()

    def schedule(self, task: Task) -> None:
        self._queue.push(task)

    def next_task(self) -> Optional[Task]:
        if self._queue.is_empty():
            return None
        return self._queue.pop()

    def pending_count(self) -> int:
        return self._queue.size()


class ResourceScheduler:
    """Resource scheduler allocating and tracking CPU, GPU, VRAM, and RAM budgets."""

    def __init__(self, cpu_cores: int = 8, memory_mb: int = 16384, vram_mb: int = 8192):
        self.limits: Dict[ResourceType, float] = {
            ResourceType.CPU: float(cpu_cores),
            ResourceType.RAM: float(memory_mb),
            ResourceType.VRAM: float(vram_mb),
        }
        self.allocated: Dict[ResourceType, float] = {
            ResourceType.CPU: 0.0,
            ResourceType.RAM: 0.0,
            ResourceType.VRAM: 0.0,
        }

    def allocate(self, resource_type: ResourceType, amount: float) -> bool:
        if resource_type not in self.limits:
            return True
        if self.allocated[resource_type] + amount <= self.limits[resource_type]:
            self.allocated[resource_type] += amount
            return True
        return False

    def release(self, resource_type: ResourceType, amount: float) -> None:
        if resource_type in self.allocated:
            self.allocated[resource_type] = max(0.0, self.allocated[resource_type] - amount)


class GPUScheduler(ResourceScheduler):
    """GPU workload scheduler managing VRAM allocations."""

    def __init__(self, total_vram_mb: int = 8192):
        super().__init__(vram_mb=total_vram_mb)

    def reserve_vram(self, amount_mb: float) -> bool:
        return self.allocate(ResourceType.VRAM, amount_mb)

    def free_vram(self, amount_mb: float) -> None:
        self.release(ResourceType.VRAM, amount_mb)


class TaskScheduler:
    """Task execution scheduler wrapping TaskExecutor."""

    def __init__(self, max_workers: int = 8):
        self.executor = TaskExecutor(max_workers=max_workers)
        self.scheduled_tasks: Dict[str, Task] = {}

    def submit_task(self, task: Task) -> asyncio.Future:
        self.scheduled_tasks[task.task_id] = task
        return self.executor.submit(task.func, *task.args, **task.kwargs)


class AgentScheduler:
    """Scheduler coordinating multi-agent execution priority."""

    def __init__(self):
        self.active_agents: Dict[str, Priority] = {}

    def register_agent(self, agent_id: str, priority: Priority = Priority.MEDIUM) -> None:
        self.active_agents[agent_id] = priority

    def get_highest_priority_agent(self) -> Optional[str]:
        if not self.active_agents:
            return None
        return max(self.active_agents, key=lambda k: self.active_agents[k].value)


class ModelScheduler:
    """Model load/unload scheduler balancing active LLM memory footprints."""

    def __init__(self, max_loaded_models: int = 3):
        self.max_loaded_models = max_loaded_models
        self.loaded_models: List[str] = []

    def load_model(self, model_id: str) -> Optional[str]:
        evicted = None
        if len(self.loaded_models) >= self.max_loaded_models:
            evicted = self.loaded_models.pop(0)
            logger.info(f"ModelScheduler evicting model '{evicted}' to load '{model_id}'")
        self.loaded_models.append(model_id)
        return evicted


class InferenceScheduler:
    """Scheduler routing inference requests across batchers and continuous queues."""

    def __init__(self):
        self.pending_requests: List[Dict[str, Any]] = []

    def queue_request(self, request: Dict[str, Any]) -> None:
        self.pending_requests.append(request)

    def pop_batch(self, batch_size: int = 16) -> List[Dict[str, Any]]:
        batch = self.pending_requests[:batch_size]
        self.pending_requests = self.pending_requests[batch_size:]
        return batch


class ContextScheduler:
    """Context window memory scheduler pruning/sliding long contexts."""

    def __init__(self, max_tokens: int = 8192):
        self.max_tokens = max_tokens

    def fit_context(self, tokens: List[int]) -> List[int]:
        if len(tokens) > self.max_tokens:
            return tokens[-self.max_tokens:]
        return tokens


class MemoryScheduler:
    """Memory scheduler scheduling periodic background consolidation and decay."""

    def __init__(self, consolidation_interval_seconds: float = 60.0):
        self.consolidation_interval_seconds = consolidation_interval_seconds
        self.last_run: float = 0.0

    def should_consolidate(self, current_time: float) -> bool:
        if current_time - self.last_run >= self.consolidation_interval_seconds:
            self.last_run = current_time
            return True
        return False


class KernelScheduler:
    """Master AI Kernel Scheduler orchestrating task, resource, agent, model, and memory schedulers."""

    def __init__(self, policy: SchedulerPolicy = SchedulerPolicy.PRIORITY):
        self.policy = policy
        self.priority_scheduler = PriorityScheduler()
        self.resource_scheduler = ResourceScheduler()
        self.gpu_scheduler = GPUScheduler()
        self.task_scheduler = TaskScheduler()
        self.agent_scheduler = AgentScheduler()
        self.model_scheduler = ModelScheduler()
        self.inference_scheduler = InferenceScheduler()
        self.context_scheduler = ContextScheduler()
        self.memory_scheduler = MemoryScheduler()

    def schedule_task(self, task: Task) -> None:
        self.priority_scheduler.schedule(task)
        logger.debug(f"KernelScheduler queued task '{task.task_id}' with priority {task.priority}")
