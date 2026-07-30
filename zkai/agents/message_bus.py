"""MessageBus and AgentMessage for inter-agent communication."""

from dataclasses import dataclass, field
import datetime
from typing import Any, Callable, Dict, List


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    content: Any
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class MessageBus:
    """Pub/Sub message bus enabling agents to send messages asynchronously."""

    def __init__(self):
        self.listeners: Dict[str, List[Callable[[AgentMessage], None]]] = {}

    def subscribe(self, agent_name: str, callback: Callable[[AgentMessage], None]) -> None:
        if agent_name not in self.listeners:
            self.listeners[agent_name] = []
        self.listeners[agent_name].append(callback)

    def send_message(self, message: AgentMessage) -> None:
        if message.recipient in self.listeners:
            for cb in self.listeners[message.recipient]:
                cb(message)
