"""Enum definitions and types for the ZKAI AI Kernel."""

from enum import Enum


class ProcessState(str, Enum):
    """Lifecycle state of managed AI Processes."""
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    RESTARTING = "restarting"


class ServiceState(str, Enum):
    """Lifecycle state of managed AI OS Services."""
    REGISTERED = "registered"
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class ResourceType(str, Enum):
    """Resource types managed by the Kernel Resource Scheduler."""
    CPU = "cpu"
    GPU = "gpu"
    VRAM = "vram"
    RAM = "ram"
    DISK = "disk"
    NETWORK = "network"
    MODEL = "model"
    AGENT = "agent"
    CONTEXT = "context"


class SchedulerPolicy(str, Enum):
    """Scheduling policies supported by the AI Kernel Scheduler."""
    FIFO = "fifo"
    PRIORITY = "priority"
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    AFFINITY = "affinity"


class KernelState(str, Enum):
    """Formal lifecycle states of the AI Kernel State Machine."""
    OFFLINE = "OFFLINE"
    BOOTING = "BOOTING"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    BUSY = "BUSY"
    IDLE = "IDLE"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"
    RECOVERY = "RECOVERY"
    UPDATING = "UPDATING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    PANIC = "PANIC"


class BootPhase(str, Enum):
    """Phases during AI Kernel deterministic boot loader execution."""
    PRE_BOOT = "PRE_BOOT"
    HARDWARE_DISCOVERY = "HARDWARE_DISCOVERY"
    SECURITY_INITIALIZATION = "SECURITY_INITIALIZATION"
    CORE_SERVICES = "CORE_SERVICES"
    SUBSYSTEM_MOUNT = "SUBSYSTEM_MOUNT"
    NETWORK_CLUSTER = "NETWORK_CLUSTER"
    POST_BOOT_VERIFICATION = "POST_BOOT_VERIFICATION"


class ShutdownMode(str, Enum):
    """Shutdown modes for kernel termination."""
    GRACEFUL = "GRACEFUL"
    EMERGENCY = "EMERGENCY"
    RESTART = "RESTART"

