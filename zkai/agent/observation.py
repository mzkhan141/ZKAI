"""Observation and ObservationParser."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Observation:
    source_action_id: str
    raw_output: Any
    parsed_summary: str


class ObservationParser:
    """Parses environment tool execution outputs into observations."""

    def parse(self, action_id: str, raw_output: Any) -> Observation:
        return Observation(
            source_action_id=action_id,
            raw_output=raw_output,
            parsed_summary=str(raw_output)[:200],
        )
