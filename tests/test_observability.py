"""Unit tests for Observability Platform, MetricsRegistry, DistributedTracer, CrashReporter, etc."""

import pytest
from zkai.kernel import (
    AIKernel,
    CrashReporter,
    DiagnosticsCenter,
    DistributedTracer,
    ExceptionAnalyzer,
    HealthDashboard,
    MetricsRegistry,
    SystemInspector,
)


def test_distributed_tracer():
    tracer = DistributedTracer()
    span1 = tracer.start_span("workflow_exec", tags={"user": "admin"})
    assert span1.span_id in tracer.spans
    
    span2 = tracer.start_span("node_exec", parent_span_id=span1.span_id)
    assert span2.parent_span_id == span1.span_id
    
    tracer.end_span(span1.span_id)
    assert tracer.spans[span1.span_id].end_time is not None


def test_crash_reporter_and_analyzer():
    reporter = CrashReporter()
    try:
        raise ValueError("Invalid configuration parameter")
    except ValueError as e:
        report = reporter.record_crash(e)
    
    assert report.exception_type == "ValueError"
    freq = ExceptionAnalyzer.analyze(reporter.reports)
    assert freq.get("ValueError") == 1


def test_diagnostics_and_inspector():
    metrics = MetricsRegistry()
    tracer = DistributedTracer()
    center = DiagnosticsCenter(metrics, tracer)
    report = center.generate_report()
    assert report["status"] == "healthy"

    kernel = AIKernel()
    inspection = SystemInspector.inspect(kernel)
    assert "kernel_state" in inspection
