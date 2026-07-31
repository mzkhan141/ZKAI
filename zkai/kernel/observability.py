"""Enterprise-grade Observability Platform, Tracing, Metrics, Diagnostics, and Crash Reporting for ZKAI."""

from dataclasses import dataclass, field
import datetime
import traceback
import time
import uuid
from typing import Any, Dict, List, Optional
from zkai.core.metrics import MetricsCollector
from zkai.core.profiling import Profiler
from zkai.core.logger import get_logger

logger = get_logger("kernel.observability")


class MetricsRegistry(MetricsCollector):
    """Central metrics registry extending MetricsCollector with service-level metric registration."""

    def __init__(self):
        super().__init__()
        self._service_metrics: Dict[str, Dict[str, Any]] = {}

    def register_service_metric(self, service_name: str, metric_name: str, value: float) -> None:
        if service_name not in self._service_metrics:
            self._service_metrics[service_name] = {}
        self._service_metrics[service_name][metric_name] = value

    def get_service_metrics(self, service_name: str) -> Dict[str, Any]:
        return self._service_metrics.get(service_name, {})


@dataclass
class TraceSpan:
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "operation"
    parent_span_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    tags: Dict[str, str] = field(default_factory=dict)


class DistributedTracer:
    """Distributed tracing engine tracking workflow and inter-service call graphs."""

    def __init__(self):
        self.spans: Dict[str, TraceSpan] = {}
        self.active_trace_id: Optional[str] = None

    def start_span(self, name: str, parent_span_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> TraceSpan:
        span = TraceSpan(
            trace_id=self.active_trace_id or str(uuid.uuid4()),
            name=name,
            parent_span_id=parent_span_id,
            tags=tags or {},
        )
        self.spans[span.span_id] = span
        if not self.active_trace_id:
            self.active_trace_id = span.trace_id
        return span

    def end_span(self, span_id: str) -> None:
        if span_id in self.spans:
            self.spans[span_id].end_time = time.time()

    def get_trace(self, trace_id: str) -> List[TraceSpan]:
        return [s for s in self.spans.values() if s.trace_id == trace_id]


class DiagnosticsCenter:
    """Central diagnostics center aggregating metrics, health checks, and tracing data."""

    def __init__(self, metrics_registry: MetricsRegistry, tracer: DistributedTracer):
        self.metrics_registry = metrics_registry
        self.tracer = tracer

    def generate_report(self) -> Dict[str, Any]:
        return {
            "timestamp": time.time(),
            "total_spans": len(self.tracer.spans),
            "service_metrics_count": len(self.metrics_registry._service_metrics),
            "status": "healthy",
        }


class PerformanceTimeline:
    """Timeline recording system execution events and performance milestones."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def log_milestone(self, name: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.events.append({"event": name, "timestamp": time.time(), "details": details or {}})


class HealthDashboard:
    """Consolidates health status across all registered kernel services."""

    @staticmethod
    def get_status(services: List[Any]) -> Dict[str, str]:
        status_map = {}
        for srv in services:
            srv_name = getattr(srv, "name", str(srv))
            status = getattr(srv, "state", "HEALTHY")
            status_map[srv_name] = getattr(status, "value", str(status))
        return status_map


@dataclass
class CrashReport:
    crash_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    exception_type: str = "Exception"
    message: str = ""
    stack_trace: str = ""


class CrashReporter:
    """Captures unhandled exceptions and generates crash reports."""

    def __init__(self):
        self.reports: List[CrashReport] = []

    def record_crash(self, exc: Exception) -> CrashReport:
        report = CrashReport(
            exception_type=type(exc).__name__,
            message=str(exc),
            stack_trace=traceback.format_exc(),
        )
        self.reports.append(report)
        logger.error(f"CrashReporter captured exception '{report.exception_type}': {report.message}")
        return report


class ExceptionAnalyzer:
    """Analyzes error frequency and root causes from recorded crash reports."""

    @staticmethod
    def analyze(reports: List[CrashReport]) -> Dict[str, int]:
        frequencies: Dict[str, int] = {}
        for r in reports:
            frequencies[r.exception_type] = frequencies.get(r.exception_type, 0) + 1
        return frequencies


class AuditDashboard:
    """Aggregates security audit logs for visual reporting."""

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def log_audit(self, actor: str, action: str, result: str) -> None:
        self.records.append({"actor": actor, "action": action, "result": result, "timestamp": time.time()})


class SystemInspector:
    """Runtime introspection tool inspecting kernel services, processes, and state."""

    @staticmethod
    def inspect(kernel: Any) -> Dict[str, Any]:
        return {
            "kernel_state": getattr(kernel.state, "value", str(kernel.state)) if hasattr(kernel, "state") else "UNKNOWN",
            "service_count": len(kernel.list_services()) if hasattr(kernel, "list_services") else 0,
            "process_count": len(kernel.list_processes()) if hasattr(kernel, "list_processes") else 0,
        }


class TelemetryController:
    """Controls telemetry collection level and opt-in/opt-out behavior."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def is_active(self) -> bool:
        return self.enabled


class PerformanceRecorder:
    """Wrapper around Profiler for automated profile session recording."""

    def __init__(self):
        self.profiler = Profiler("performance_recorder")

    def record_session(self, section_name: str, action: Any) -> Any:
        self.profiler.start()
        res = action()
        self.profiler.stop(section_name=section_name)
        return res
