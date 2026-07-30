"""Universal Knowledge Bus, Intent Bus, Semantic Events, and Context Propagation for ZKAI."""

from dataclasses import dataclass, field
import time
from typing import Any, Callable, Dict, List, Optional
from zkai.core.events import Event, EventBus, default_event_bus
from zkai.core.logger import get_logger

logger = get_logger("ipc.knowledge_bus")


@dataclass
class SemanticEvent(Event):
    """Base semantic event carrying rich knowledge context."""
    intent: str = "general"
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningEvent(SemanticEvent):
    hypothesis: str = ""
    confidence: float = 1.0


@dataclass
class MemoryEvent(SemanticEvent):
    key: str = ""
    memory_type: str = "working"


@dataclass
class CapabilityEvent(SemanticEvent):
    capability_name: str = ""
    granted: bool = True


@dataclass
class GoalEvent(SemanticEvent):
    goal_id: str = ""
    objective: str = ""


@dataclass
class LearningEvent(SemanticEvent):
    metric: str = ""
    improvement_delta: float = 0.0


class ContextPropagator:
    """Propagates semantic context tokens across message calls."""

    def __init__(self):
        self.active_context: Dict[str, Any] = {}

    def set_context(self, key: str, value: Any) -> None:
        self.active_context[key] = value

    def get_context(self) -> Dict[str, Any]:
        return dict(self.active_context)


class IntentResolver:
    """Resolves natural language or structured intents to handler callbacks."""

    def __init__(self):
        self.handlers: Dict[str, Callable[[SemanticEvent], Any]] = {}

    def register_intent(self, intent_name: str, handler: Callable[[SemanticEvent], Any]) -> None:
        self.handlers[intent_name] = handler

    def resolve(self, event: SemanticEvent) -> Any:
        if event.intent in self.handlers:
            return self.handlers[event.intent](event)
        logger.debug(f"IntentResolver: No specific handler for intent '{event.intent}'")
        return None


class SemanticDispatcher:
    """Dispatches semantic events based on meaning rather than string topic."""

    def __init__(self, resolver: IntentResolver):
        self.resolver = resolver

    def dispatch(self, event: SemanticEvent) -> Any:
        return self.resolver.resolve(event)


class KnowledgeRouter:
    """Routes semantic knowledge payloads to target knowledge stores and subsystems."""

    def __init__(self):
        self.routes: Dict[str, List[Callable[[Any], None]]] = {}

    def add_route(self, topic: str, handler: Callable[[Any], None]) -> None:
        if topic not in self.routes:
            self.routes[topic] = []
        self.routes[topic].append(handler)

    def route(self, topic: str, payload: Any) -> None:
        for handler in self.routes.get(topic, []):
            handler(payload)


class IntentBus:
    """High-level bus dedicated to intention-based agent requests."""

    def __init__(self):
        self.resolver = IntentResolver()

    def post_intent(self, intent_name: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        evt = SemanticEvent(intent=intent_name, payload=payload or {})
        return self.resolver.resolve(evt)


class KnowledgeBus:
    """Universal Knowledge Bus connecting all OS subsystems via semantic events."""

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.event_bus = event_bus or default_event_bus
        self.router = KnowledgeRouter()
        self.intent_bus = IntentBus()
        self.context = ContextPropagator()

    def publish_semantic(self, event: SemanticEvent) -> None:
        self.event_bus.publish(event)
        self.intent_bus.resolver.resolve(event)
        logger.debug(f"KnowledgeBus published semantic event (intent: '{event.intent}')")
