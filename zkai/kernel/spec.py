"""Architecture Decision Records and Markdown Documentation Generator for ZKAI OS."""

import inspect
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("kernel.spec")


class ArchitectureSpec:
    """Generates Architecture Decision Records (ADRs) and master architecture spec markdown files."""

    def __init__(self, output_dir: str = "./docs"):
        self.output_dir = Path(output_dir)

    def generate_all(self) -> List[str]:
        """Generates full suite of markdown architecture documents."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        generated_files = []

        files_map = {
            "architecture_decision_records.md": self.generate_adr(),
            "kernel_specification.md": KernelSpec().generate(),
            "public_api_specification.md": PublicAPISpec().generate(),
            "plugin_specification.md": PluginSpec().generate(),
            "service_specification.md": ServiceSpec().generate(),
            "workflow_specification.md": WorkflowSpec().generate(),
            "memory_specification.md": MemorySpec().generate(),
            "security_specification.md": SecuritySpec().generate(),
            "serialization_specification.md": SerializationSpec().generate(),
            "zk_file_format_specification.md": self.generate_zk_format_spec(),
            "compatibility_specification.md": CompatibilitySpec().generate(),
            "dependency_graph.md": DependencyGraphDoc().generate(),
        }

        for filename, content in files_map.items():
            path = self.output_dir / filename
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            generated_files.append(str(path))
            logger.info(f"Generated Architecture Specification: {path}")

        return generated_files

    def generate_adr(self) -> str:
        return (
            "# ZKAI Architecture Decision Record (ADR)\n\n"
            "## ADR-001: Kernel-Centric AI Operating System Architecture\n"
            "- **Status**: Accepted\n"
            "- **Context**: ZKAI manages **Intelligence** as its primary system resource.\n"
            "- **Decision**: Every subsystem (process, IPC, filesystem, memory, security, cluster, voice, etc.) is registered as a Kernel Service under the AIKernel singleton.\n"
            "- **Consequences**: Deterministic boot order, capability security, transactional snapshots, fair resource governance.\n"
        )

    def generate_zk_format_spec(self) -> str:
        return (
            "# ZK Binary Container (.zk) Format Specification\n\n"
            "## Layout\n"
            "- Magic Bytes: `ZKAI` (4 bytes)\n"
            "- Version: uint16\n"
            "- Header Length: uint32\n"
            "- JSON Metadata Header\n"
            "- PyTorch State Dict Tensor Payload\n"
        )


class ModuleSpec:
    """Auto-introspects Python modules and generates structured markdown specs."""

    @staticmethod
    def generate_for_module(module: Any) -> str:
        name = getattr(module, "__name__", "Module")
        doc = getattr(module, "__doc__", "") or "No module docstring."
        classes = [name for name, cls in inspect.getmembers(module, inspect.isclass)]
        return f"# Module Specification: `{name}`\n\n{doc}\n\n## Exported Classes\n" + "\n".join(f"- `{c}`" for c in classes) + "\n"


class KernelSpec:
    """Generates AI Kernel specification markdown."""

    def generate(self) -> str:
        return (
            "# AI Kernel Specification\n\n"
            "The AI Kernel orchestrates process scheduling, memory governance, IPC routing, identity, capability security, and hardware abstraction.\n"
        )


class PublicAPISpec:
    """Generates Public API specification markdown."""

    def generate(self) -> str:
        return (
            "# ZKAI Public API Specification\n\n"
            "Single unified entry point:\n"
            "```python\n"
            "from zkai import *\n"
            "ai = ZKAI()\n"
            "```\n"
        )


class PluginSpec:
    """Generates Plugin system specification markdown."""

    def generate(self) -> str:
        return "# Plugin System Specification\n\nPlugins extend ZKAI using PluginManifest, PluginSandbox, and HotReloader.\n"


class ServiceSpec:
    """Generates OS Service specification markdown."""

    def generate(self) -> str:
        return "# OS Service Specification\n\nManaged services subclass `Service` and register with `AIKernel.register_service()`.\n"


class WorkflowSpec:
    """Generates Workflow engine specification markdown."""

    def generate(self) -> str:
        return "# Workflow Engine Specification\n\nDAG workflows execute using WorkflowNode, ActionNode, Conditional, Retry, and HumanApproval.\n"


class MemorySpec:
    """Generates 14-subsystem Memory OS specification markdown."""

    def generate(self) -> str:
        return "# Memory OS Specification\n\nSupports 14 memory taxonomy types, FAISS vector search, and background MemoryDaemon consolidation.\n"


class SecuritySpec:
    """Generates Security Kernel specification markdown."""

    def generate(self) -> str:
        return "# Security Kernel Specification\n\nCapability-based security with 21 capabilities, Fernet encryption, and AuditLog.\n"


class SerializationSpec:
    """Generates ZKSerializer specification markdown."""

    def generate(self) -> str:
        return "# Serialization Specification\n\nZKSerializer handles binary containers, JSON headers, and backward-compatible schemas.\n"


class CompatibilitySpec:
    """Generates ecosystem compatibility specification markdown."""

    def generate(self) -> str:
        return "# Ecosystem Compatibility Specification\n\nProvides seamless compatibility layers for HuggingFace, ONNX, GGUF, TensorRT, Safetensors, and OpenVINO.\n"


class DependencyGraphDoc:
    """Generates Dependency Graph documentation markdown."""

    def generate(self) -> str:
        return "# ZKAI Subsystem Dependency Graph\n\n```mermaid\ngraph TD\n  Kernel --> ProcessManager\n  Kernel --> ServiceManager\n  Kernel --> SecurityKernel\n  Kernel --> MemoryOS\n  Kernel --> ResourceGovernor\n```\n"
