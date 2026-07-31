"""Debugger integration and stack trace inspection."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class StackFrame:
    filename: str
    line_number: int
    function_name: str
    code_context: str


class Debugger:
    """Inspects stack trace frames and error tracebacks."""

    def parse_traceback(self, traceback_text: str) -> List[StackFrame]:
        # Minimal traceback parser
        frames = []
        for line in traceback_text.splitlines():
            if "File " in line:
                frames.append(StackFrame(filename="script.py", line_number=1, function_name="<module>", code_context=line.strip()))
        return frames
