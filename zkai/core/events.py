"""Asynchronous Event Bus System and built-in event definitions for ZKAI."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union
from zkai.core.logger import get_logger

logger = get_logger("events")


@dataclass
class Event:
    """Base class for all system and custom events in ZKAI."""
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "zkai"
    metadata: Dict[str, Any] = field(default_factory=dict)


# --- Built-in Model & Inference Events ---
@dataclass
class BeforeModelLoad(Event):
    model_name: str = ""
    device: str = ""


@dataclass
class AfterModelLoad(Event):
    model_name: str = ""
    load_time_seconds: float = 0.0


@dataclass
class BeforeInference(Event):
    prompt: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AfterInference(Event):
    prompt: str = ""
    response: str = ""
    token_count: int = 0
    duration_seconds: float = 0.0


# --- Built-in Tool & Agent Events ---
@dataclass
class ToolStarted(Event):
    tool_name: str = ""
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolFinished(Event):
    tool_name: str = ""
    result: Any = None
    success: bool = True
    error: str = ""


@dataclass
class TaskStarted(Event):
    task_id: str = ""
    goal: str = ""


@dataclass
class TaskFinished(Event):
    task_id: str = ""
    status: str = "completed"
    result: Any = None


# --- Built-in Memory Events ---
@dataclass
class MemoryStored(Event):
    memory_type: str = ""
    key: str = ""
    content: Any = None


@dataclass
class MemoryRetrieved(Event):
    query: str = ""
    relevance_scores: List[float] = field(default_factory=list)


# --- Built-in Capability Events ---
@dataclass
class BrowserOpened(Event):
    url: str = ""


@dataclass
class CodeExecuted(Event):
    language: str = "python"
    code: str = ""
    success: bool = True
    output: str = ""


@dataclass
class FileSaved(Event):
    file_path: str = ""
    size_bytes: int = 0


# --- Signal Definition ---
@dataclass
class Signal(Event):
    """Lightweight signal event with a name and optional payload."""
    name: str = "signal"
    data: Any = None


E = TypeVar("E", bound=Event)
EventHandler = Callable[[Any], Union[None, Any]]


class EventBus:
    """Central Asynchronous Event Bus supporting publish-subscribe pattern."""

    def __init__(self):
        self._handlers: Dict[Type[Event], List[EventHandler]] = {}
        self._history: List[Event] = []
        self._persistent_log: Optional["PersistentEventLog"] = None

    def set_persistent_log(self, persistent_log: "PersistentEventLog") -> None:
        """Attaches a persistent log recorder to the event bus."""
        self._persistent_log = persistent_log

    def subscribe(self, event_type: Type[E], handler: EventHandler) -> None:
        """Subscribes an async or sync handler to a specific event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.debug(f"Subscribed handler '{getattr(handler, '__name__', str(handler))}' to '{event_type.__name__}'")

    def unsubscribe(self, event_type: Type[E], handler: EventHandler) -> None:
        """Unsubscribes a handler from a specific event type."""
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

    async def publish_async(self, event: Event) -> None:
        """Publishes an event asynchronously to all subscribed listeners."""
        self._history.append(event)
        if self._persistent_log:
            self._persistent_log.record(event)

        event_type = type(event)
        handlers = self._handlers.get(event_type, [])
        # Also include generic Event subscribers if subscribed to base Event
        if event_type is not Event and Event in self._handlers:
            handlers = handlers + self._handlers[Event]

        logger.debug(f"Publishing event '{event_type.__name__}' to {len(handlers)} handlers")

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error executing event handler '{getattr(handler, '__name__', str(handler))}' for '{event_type.__name__}': {e}")

    def publish(self, event: Event) -> None:
        """Synchronous wrapper for publishing events."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.publish_async(event))
        except RuntimeError:
            asyncio.run(self.publish_async(event))

    def get_history(self) -> List[Event]:
        """Returns in-memory event history."""
        return list(self._history)

    def replay_history(self, event_type: Optional[Type[Event]] = None) -> None:
        """Replays historical events back into handlers."""
        for evt in self._history:
            if event_type is None or isinstance(evt, event_type):
                self.publish(evt)


class Publisher:
    """Convenience publisher bound to a specific source and event bus."""

    def __init__(self, source: str = "publisher", bus: Optional[EventBus] = None):
        self.source = source
        self.bus = bus or default_event_bus

    def publish(self, event: Event) -> None:
        event.source = self.source
        self.bus.publish(event)

    async def publish_async(self, event: Event) -> None:
        event.source = self.source
        await self.bus.publish_async(event)


class Subscriber:
    """Subscriber wrapper for auto-subscribing and filtering events."""

    def __init__(self, bus: Optional[EventBus] = None):
        self.bus = bus or default_event_bus
        self._subscriptions: List[Tuple[Type[Event], EventHandler]] = []

    def listen(self, event_type: Type[E], filter_fn: Optional[Callable[[E], bool]] = None) -> Callable[[EventHandler], EventHandler]:
        def decorator(handler: EventHandler) -> EventHandler:
            def wrapper(event: E) -> Any:
                if filter_fn is None or filter_fn(event):
                    return handler(event)

            self.bus.subscribe(event_type, wrapper)
            self._subscriptions.append((event_type, wrapper))
            return handler
        return decorator

    def close(self) -> None:
        """Unsubscribes all handlers managed by this subscriber."""
        for event_type, handler in self._subscriptions:
            self.bus.unsubscribe(event_type, handler)
        self._subscriptions.clear()


class Trigger:
    """Conditional trigger firing target events when predicate evaluates to True."""

    def __init__(self, predicate: Callable[[Event], bool], action: Callable[[Event], None], bus: Optional[EventBus] = None):
        self.predicate = predicate
        self.action = action
        self.bus = bus or default_event_bus
        self.bus.subscribe(Event, self._check)

    def _check(self, event: Event) -> None:
        if self.predicate(event):
            self.action(event)


class Observer:
    """Observer pattern mixin for auto-subscribing methods to event bus."""

    def register_observers(self, bus: Optional[EventBus] = None) -> None:
        bus_instance = bus or default_event_bus
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "_on_event_type"):
                event_type = getattr(attr, "_on_event_type")
                bus_instance.subscribe(event_type, attr)


def on_event(event_type: Type[Event]) -> Callable[[EventHandler], EventHandler]:
    """Decorator marking method for Observer registration."""
    def decorator(fn: EventHandler) -> EventHandler:
        setattr(fn, "_on_event_type", event_type)
        return fn
    return decorator


class PersistentEventLog:
    """JSON Lines file recorder for event persistence."""

    def __init__(self, filepath: str = "events.jsonl"):
        self.filepath = filepath

    def record(self, event: Event) -> None:
        import json
        import os
        record_data = {
            "type": event.__class__.__name__,
            "timestamp": event.timestamp.isoformat(),
            "source": event.source,
            "metadata": event.metadata,
        }
        os.makedirs(os.path.dirname(os.path.abspath(self.filepath)), exist_ok=True)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record_data) + "\n")


class EventReplay:
    """Replays persistent JSON Lines events into target event bus."""

    def __init__(self, filepath: str = "events.jsonl", bus: Optional[EventBus] = None):
        self.filepath = filepath
        self.bus = bus or default_event_bus

    def replay(self) -> int:
        import json
        import os
        if not os.path.exists(self.filepath):
            return 0
        count = 0
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    evt = Event(source=data.get("source", "replay"), metadata=data.get("metadata", {}))
                    self.bus.publish(evt)
                    count += 1
        return count


class DistributedEventBridge:
    """Bridge forwarding events across queue / IPC process boundaries."""

    def __init__(self, queue: Any = None, bus: Optional[EventBus] = None):
        self.queue = queue
        self.bus = bus or default_event_bus

    def send(self, event: Event) -> None:
        if self.queue and hasattr(self.queue, "put"):
            self.queue.put(event)
        else:
            self.bus.publish(event)

    def receive_loop(self) -> None:
        if self.queue and hasattr(self.queue, "get"):
            while not getattr(self.queue, "empty", lambda: False)():
                evt = self.queue.get()
                self.bus.publish(evt)


# Global default EventBus instance
default_event_bus = EventBus()

