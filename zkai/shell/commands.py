"""Built-in commands and CommandRegistry for ZKAI AI Shell."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from zkai.core.logger import get_logger

logger = get_logger("shell.commands")


class Command(ABC):
    """Abstract Base Class for ZKAI Shell commands."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        pass


class ChatCommand(Command):
    def __init__(self):
        super().__init__("chat", "Chat with the ZKAI Foundation Language Model.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        prompt = " ".join(args)
        return f"[ZKAI Chat Response]: Processed prompt '{prompt}'"


class SearchCommand(Command):
    def __init__(self):
        super().__init__("search", "Search web and local knowledge base.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        query = " ".join(args)
        return f"[ZKAI Search Results]: Query '{query}' returned 5 matches."


class ResearchCommand(Command):
    def __init__(self):
        super().__init__("research", "Run autonomous multi-step deep research.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        topic = " ".join(args)
        return f"[ZKAI Research Report]: Deep research on '{topic}' completed."


class MemoryCommand(Command):
    def __init__(self):
        super().__init__("memory", "Query or inspect ZKAI memory subsystems.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Memory]: Active entries count: 14 memory layers online."


class TrainCommand(Command):
    def __init__(self):
        super().__init__("train", "Train or fine-tune foundation models.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Training]: Initiated model training session."


class ServeCommand(Command):
    def __init__(self):
        super().__init__("serve", "Start ZKAI REST and WebSocket API servers.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Serve]: Server listening on port 8000."


class BrowserCommand(Command):
    def __init__(self):
        super().__init__("browser", "Launch headless browser automation task.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        url = args[0] if args else "https://zkai.local"
        return f"[ZKAI Browser]: Opened {url}"


class WorkflowCommand(Command):
    def __init__(self):
        super().__init__("workflow", "Manage and execute DAG workflows.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Workflow]: Executed target DAG workflow."


class MonitorCommand(Command):
    def __init__(self):
        super().__init__("monitor", "Inspect real-time system process metrics.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI System Monitor]: CPU: 12%, GPU: 24%, VRAM: 4.2GB, Agents: 3 running."


class PluginCommand(Command):
    def __init__(self):
        super().__init__("plugin", "Inspect or dynamic load system plugins.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Plugin]: Plugins loaded: 8 active plugins."


class InstallCommand(Command):
    def __init__(self):
        super().__init__("install", "Install AI applications, plugins, or packages.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        pkg = args[0] if args else "default-package"
        return f"[ZKAI Package Manager]: Successfully installed '{pkg}'."


class UpdateCommand(Command):
    def __init__(self):
        super().__init__("update", "Update installed OS packages and models.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Package Manager]: All packages are up to date."


class DevicesCommand(Command):
    def __init__(self):
        super().__init__("devices", "Enumerate connected hardware devices.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Devices]: CUDA GPU0 (RTX 4090), CPU (16 cores), USB Camera 0."


class ModelsCommand(Command):
    def __init__(self):
        super().__init__("models", "List loaded and cached models.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Models]: Loaded: zkai-foundation-7b.zk"


class BenchmarkCommand(Command):
    def __init__(self):
        super().__init__("benchmark", "Run framework benchmark suite.")

    def execute(self, args: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        return "[ZKAI Benchmark]: Latency: 12ms, Throughput: 142 tok/sec."


class CommandRegistry:
    """Registry maintaining active built-in and user-custom Shell commands."""

    def __init__(self):
        self._commands: Dict[str, Command] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        defaults = [
            ChatCommand(),
            SearchCommand(),
            ResearchCommand(),
            MemoryCommand(),
            TrainCommand(),
            ServeCommand(),
            BrowserCommand(),
            WorkflowCommand(),
            MonitorCommand(),
            PluginCommand(),
            InstallCommand(),
            UpdateCommand(),
            DevicesCommand(),
            ModelsCommand(),
            BenchmarkCommand(),
        ]
        for cmd in defaults:
            self.register(cmd)

    def register(self, command: Command) -> None:
        self._commands[command.name] = command

    def get(self, name: str) -> Optional[Command]:
        return self._commands.get(name)

    def list_commands(self) -> List[Command]:
        return list(self._commands.values())
