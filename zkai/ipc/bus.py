"""SystemMessageBus extending EventBus for typed interprocess communication."""

from dataclasses import dataclass, field
import datetime
from typing import Any, Callable, Dict, List, Optional
from zkai.core.events import Event, EventBus, default_event_bus
from zkai.core.logger import get_logger

logger = get_logger("ipc.bus")


@dataclass
class IPCMessage(Event):
    """Base message for interprocess communication."""
    topic: str = "general"
    payload: Any = None
    sender_id: str = "system"
    recipient_id: str = "*"


import threading


class SystemMessageBus:
    """System message bus managing IPC routing across processes with thread-safe lock protection."""

    def __init__(self, bus: Optional[EventBus] = None):
        self.bus = bus or default_event_bus
        self._topic_listeners: Dict[str, List[Callable[[IPCMessage], None]]] = {}
        self._lock = threading.Lock()

    def subscribe_topic(self, topic: str, handler: Callable[[IPCMessage], None]) -> None:
        with self._lock:
            if topic not in self._topic_listeners:
                self._topic_listeners[topic] = []
            self._topic_listeners[topic].append(handler)

    def publish_message(self, message: IPCMessage) -> None:
        self.bus.publish(message)
        with self._lock:
            handlers = list(self._topic_listeners.get(message.topic, []))
        for handler in handlers:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Error handling IPC message on topic '{message.topic}': {e}")
