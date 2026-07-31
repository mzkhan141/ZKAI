"""Configuration model for the AI Kernel."""

from pydantic import BaseModel, Field
from zkai.kernel.types import SchedulerPolicy


class KernelConfig(BaseModel):
    """Configuration settings for the AI Kernel runtime and schedulers."""
    heartbeat_interval: float = 2.0
    scheduler_policy: SchedulerPolicy = SchedulerPolicy.PRIORITY
    max_processes: int = 128
    tick_rate_hz: int = 10
    persistence_path: str = "./kernel_state.json"
    auto_boot_services: bool = True
    enable_watchdog: bool = True
