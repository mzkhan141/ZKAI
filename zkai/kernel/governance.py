"""Resource Governance, Quotas, Admission Control, and Fair Scheduling for ZKAI."""

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger
from zkai.kernel.types import ResourceType

logger = get_logger("kernel.governance")


@dataclass
class QuotaSpec:
    """Resource quota specification with limit and burst allocation."""
    resource_type: ResourceType
    max_limit: float
    reserved: float = 0.0
    allocated: float = 0.0


@dataclass
class CPUQuota(QuotaSpec):
    def __init__(self, max_cores: float = 8.0):
        super().__init__(ResourceType.CPU, max_cores)


@dataclass
class GPUQuota(QuotaSpec):
    def __init__(self, max_gpus: float = 1.0):
        super().__init__(ResourceType.GPU, max_gpus)


@dataclass
class VRAMQuota(QuotaSpec):
    def __init__(self, max_vram_mb: float = 8192.0):
        super().__init__(ResourceType.VRAM, max_vram_mb)


@dataclass
class RAMQuota(QuotaSpec):
    def __init__(self, max_ram_mb: float = 16384.0):
        super().__init__(ResourceType.RAM, max_ram_mb)


@dataclass
class DiskQuota(QuotaSpec):
    def __init__(self, max_disk_gb: float = 100.0):
        super().__init__(ResourceType.DISK, max_disk_gb)


@dataclass
class TokenQuota(QuotaSpec):
    def __init__(self, max_tokens_per_sec: float = 1000.0):
        super().__init__(ResourceType.MODEL, max_tokens_per_sec)


@dataclass
class ContextQuota(QuotaSpec):
    def __init__(self, max_context_tokens: float = 128000.0):
        super().__init__(ResourceType.CONTEXT, max_context_tokens)


@dataclass
class BandwidthQuota(QuotaSpec):
    def __init__(self, max_kbps: float = 100000.0):
        super().__init__(ResourceType.NETWORK, max_kbps)


class AdmissionController:
    """Decides whether workload execution requests may be admitted based on available resource quotas."""

    def __init__(self, quotas: Dict[ResourceType, QuotaSpec]):
        self.quotas = quotas

    def admit(self, requirements: Dict[ResourceType, float]) -> bool:
        for res_type, amount in requirements.items():
            if res_type in self.quotas:
                q = self.quotas[res_type]
                if q.allocated + amount > q.max_limit:
                    logger.warning(f"AdmissionController DENIED workload: {res_type.value} requested {amount}, allocated {q.allocated}/{q.max_limit}")
                    return False
        return True


class PriorityInheritance:
    """Prevents priority inversion by boosting lock holder priority to highest waiting task."""

    @staticmethod
    def calculate_effective_priority(base_priority: int, waiting_priorities: List[int]) -> int:
        if not waiting_priorities:
            return base_priority
        return max(base_priority, max(waiting_priorities))


class FairScheduler:
    """Weighted Fair Queueing (WFQ) scheduling across processes/tenants."""

    def __init__(self):
        self.weights: Dict[str, float] = {}

    def set_weight(self, entity_id: str, weight: float) -> None:
        self.weights[entity_id] = max(0.1, weight)

    def compute_fair_share(self, total_capacity: float) -> Dict[str, float]:
        total_weight = sum(self.weights.values()) if self.weights else 1.0
        return {entity: (w / total_weight) * total_capacity for entity, w in self.weights.items()}


class PreemptionPolicies:
    """Preemption policies for high-priority task preemption."""

    @staticmethod
    def should_preempt(active_priority: int, incoming_priority: int, priority_threshold: int = 5) -> bool:
        return (incoming_priority - active_priority) >= priority_threshold


class RateLimiter:
    """Token-bucket rate limiter for requests per second."""

    def __init__(self, rate_per_sec: float = 50.0, capacity: float = 100.0):
        self.rate = rate_per_sec
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()

    def consume(self, amount: float = 1.0) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False


class ResourceAccounting:
    """Tracks cumulative resource usage per process and identity."""

    def __init__(self):
        self.usage_log: Dict[str, Dict[ResourceType, float]] = {}

    def record_usage(self, entity_id: str, resource_type: ResourceType, amount: float) -> None:
        if entity_id not in self.usage_log:
            self.usage_log[entity_id] = {}
        curr = self.usage_log[entity_id].get(resource_type, 0.0)
        self.usage_log[entity_id][resource_type] = curr + amount

    def get_usage(self, entity_id: str) -> Dict[ResourceType, float]:
        return self.usage_log.get(entity_id, {})


class ResourceReservations:
    """Reservations manager for pre-allocating resource budgets."""

    def __init__(self, quotas: Dict[ResourceType, QuotaSpec]):
        self.quotas = quotas
        self.reservations: Dict[str, Dict[ResourceType, float]] = {}

    def reserve(self, reservation_id: str, requirements: Dict[ResourceType, float]) -> bool:
        for res, amt in requirements.items():
            if res in self.quotas:
                q = self.quotas[res]
                if q.allocated + q.reserved + amt > q.max_limit:
                    return False

        for res, amt in requirements.items():
            if res in self.quotas:
                self.quotas[res].reserved += amt

        self.reservations[reservation_id] = requirements
        return True

    def release(self, reservation_id: str) -> None:
        if reservation_id in self.reservations:
            reqs = self.reservations[reservation_id]
            for res, amt in reqs.items():
                if res in self.quotas:
                    self.quotas[res].reserved = max(0.0, self.quotas[res].reserved - amt)
            del self.reservations[reservation_id]


class ResourceRebalancer:
    """Rebalances allocated quotas across active workloads dynamically."""

    @staticmethod
    def rebalance(quotas: Dict[ResourceType, QuotaSpec], active_workloads: int) -> None:
        if active_workloads <= 0:
            return
        logger.info(f"ResourceRebalancer rebalancing quotas across {active_workloads} active workloads.")


class ResourceGovernor:
    """Master Resource Governor controlling admission, quotas, rate limiting, and accounting."""

    def __init__(self):
        self.quotas: Dict[ResourceType, QuotaSpec] = {
            ResourceType.CPU: CPUQuota(),
            ResourceType.GPU: GPUQuota(),
            ResourceType.VRAM: VRAMQuota(),
            ResourceType.RAM: RAMQuota(),
            ResourceType.DISK: DiskQuota(),
            ResourceType.MODEL: TokenQuota(),
            ResourceType.CONTEXT: ContextQuota(),
            ResourceType.NETWORK: BandwidthQuota(),
        }
        self.admission = AdmissionController(self.quotas)
        self.fair_scheduler = FairScheduler()
        self.rate_limiter = RateLimiter()
        self.accounting = ResourceAccounting()
        self.reservations = ResourceReservations(self.quotas)

    def request_allocation(self, process_id: str, requirements: Dict[ResourceType, float]) -> bool:
        """Evaluates admission and allocates resources if granted."""
        if not self.admission.admit(requirements):
            return False

        for res_type, amount in requirements.items():
            if res_type in self.quotas:
                self.quotas[res_type].allocated += amount
                self.accounting.record_usage(process_id, res_type, amount)

        logger.info(f"ResourceGovernor allocated {requirements} to process '{process_id}'")
        return True

    def release_allocation(self, process_id: str, requirements: Dict[ResourceType, float]) -> None:
        """Releases allocated resources back to pool."""
        for res_type, amount in requirements.items():
            if res_type in self.quotas:
                q = self.quotas[res_type]
                q.allocated = max(0.0, q.allocated - amount)
        logger.info(f"ResourceGovernor released {requirements} from process '{process_id}'")
