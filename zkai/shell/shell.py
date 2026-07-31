"""Interactive REPL Shell and Command Processor for ZKAI AI Operating System."""

from typing import Any, Dict, List, Optional
from zkai.shell.commands import CommandRegistry
from zkai.core.logger import get_logger

logger = get_logger("shell")


class ZKShell:
    """Native AI Shell with script execution, aliases, history, and pipeline processing."""

    def __init__(self):
        self.registry = CommandRegistry()
        self.history: List[str] = []
        self.aliases: Dict[str, str] = {}

    def set_alias(self, alias_name: str, command_str: str) -> None:
        self.aliases[alias_name] = command_str

    def execute_line(self, line: str) -> str:
        line_clean = line.strip()
        if not line_clean:
            return ""

        self.history.append(line_clean)

        # Expand alias if matching
        tokens = line_clean.split()
        first_token = tokens[0]
        if first_token in self.aliases:
            line_clean = self.aliases[first_token] + " " + " ".join(tokens[1:])
            tokens = line_clean.split()

        # Handle piping pipeline (|)
        if "|" in line_clean:
            stages = [stage.strip() for stage in line_clean.split("|")]
            output = ""
            for stage in stages:
                stage_tokens = stage.split()
                cmd_name = stage_tokens[0]
                args = stage_tokens[1:]
                if output:
                    args.append(output)
                cmd = self.registry.get(cmd_name)
                if cmd:
                    output = cmd.execute(args)
                else:
                    return f"Unknown command in pipeline: '{cmd_name}'"
            return output

        cmd_name = tokens[0]
        args = tokens[1:]
        cmd = self.registry.get(cmd_name)
        if not cmd:
            return f"Command not found: '{cmd_name}'. Type 'help' to list commands."

        return cmd.execute(args)

    def execute_script(self, script_content: str) -> List[str]:
        """Executes a .zks multi-line script file."""
        outputs = []
        for line in script_content.splitlines():
            line_str = line.strip()
            if line_str and not line_str.startswith("#"):
                res = self.execute_line(line_str)
                outputs.append(res)
        return outputs
