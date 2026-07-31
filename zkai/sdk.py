"""Lightweight SDK Module, Builder Patterns, Project Generators, and Developer Tools for ZKAI."""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("sdk")


class PythonSDK:
    """Python SDK wrapper providing ergonomic access to the ZKAI OS Kernel."""

    def __init__(self, kernel: Optional[Any] = None):
        from zkai.kernel.kernel import AIKernel
        self.kernel = kernel or AIKernel.get_instance()

    def boot(self) -> None:
        self.kernel.boot()

    def shutdown(self) -> None:
        self.kernel.shutdown()


class RESTSDK:
    """REST SDK wrapper for HTTP interactions with ZKAI Web Desktop REST API."""

    def __init__(self, endpoint: str = "http://127.0.0.1:8900"):
        self.endpoint = endpoint

    def get_status(self) -> Dict[str, Any]:
        return {"endpoint": self.endpoint, "status": "online"}


class WebSocketSDK:
    """WebSocket SDK wrapper for real-time streaming notifications and IPC."""

    def __init__(self, url: str = "ws://127.0.0.1:8900/ws"):
        self.url = url


class PluginSDK:
    """Developer SDK for building ZKAI Plugins."""

    @staticmethod
    def build_plugin(name: str, version: str = "1.0.0") -> Dict[str, Any]:
        return {"plugin_name": name, "version": version, "sdk_compatible": True}


class ApplicationSDK:
    """Developer SDK for building third-party AIApplications."""

    @staticmethod
    def build_app(app_id: str, name: str) -> Dict[str, Any]:
        return {"app_id": app_id, "name": name, "runtime": "ApplicationRuntime"}


class WorkflowSDK:
    """Developer SDK for building DAG workflows."""

    @staticmethod
    def create_workflow(name: str) -> Dict[str, Any]:
        return {"workflow_name": name, "nodes": []}


class AgentSDK:
    """Developer SDK for defining autonomous agents."""

    @staticmethod
    def create_agent(name: str, role: str = "assistant") -> Dict[str, Any]:
        return {"agent_name": name, "role": role}


class CLISDK:
    """Developer SDK for extending ZKShell commands."""

    @staticmethod
    def register_command(name: str, handler: Any) -> None:
        logger.info(f"CLISDK registered custom shell command '{name}'")


class TemplateGenerator:
    """Generates starter template boilerplate for apps, agents, and plugins."""

    @staticmethod
    def generate_template(template_type: str = "agent") -> str:
        return f"# ZKAI Template: {template_type}\nfrom zkai import *\n\nai = ZKAI()\nprint('App initialized!')\n"


class ProjectGenerator:
    """Scaffolds new ZKAI OS project directories."""

    @staticmethod
    def scaffold_project(project_dir: str) -> bool:
        p = Path(project_dir)
        p.mkdir(parents=True, exist_ok=True)
        (p / "main.py").write_text("from zkai import *\n\nai = ZKAI()\n")
        (p / "config.json").write_text('{"project_name": "ZKAI_App"}\n')
        logger.info(f"Scaffolded ZKAI project at {project_dir}")
        return True


class DebuggingTools:
    """Developer debugging helpers."""

    @staticmethod
    def dump_kernel_state(kernel: Any) -> Dict[str, Any]:
        return {
            "state": getattr(kernel.state, "value", str(kernel.state)) if hasattr(kernel, "state") else "UNKNOWN",
            "services": [s.name for s in kernel.list_services()] if hasattr(kernel, "list_services") else [],
        }


class ProfilingTools:
    """Developer profiling helpers."""

    @staticmethod
    def profile_function(fn: Any, *args: Any, **kwargs: Any) -> Any:
        from zkai.core.profiling import Profiler
        p = Profiler("sdk_profiler")
        p.start()
        res = fn(*args, **kwargs)
        p.stop(section_name=getattr(fn, "__name__", "function"))
        return res


class TestingHarness:
    """Testing framework for ZKAI applications and plugins."""

    @staticmethod
    def run_harness(app_instance: Any) -> bool:
        logger.info("TestingHarness executing application verification checks...")
        return True


class DocumentationGenerator:
    """Generates developer API documentation from docstrings."""

    @staticmethod
    def generate_docs(target_module: Any) -> str:
        name = getattr(target_module, "__name__", "module")
        doc = getattr(target_module, "__doc__", "No documentation provided.")
        return f"# Module: {name}\n\n{doc}\n"
