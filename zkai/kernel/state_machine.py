"""Formal Kernel Lifecycle State Machine and Transition Management for ZKAI."""

from dataclasses import dataclass, field
import time
from typing import Any, Callable, Dict, List, Optional, Set
from zkai.core.events import Event, EventBus, default_event_bus
from zkai.core.logger import get_logger
from zkai.kernel.types import KernelState

logger = get_logger("kernel.state_machine")


@dataclass
class KernelEvents(Event):
    """Event published on formal kernel state machine transitions."""
    previous_state: KernelState = KernelState.OFFLINE
    current_state: KernelState = KernelState.OFFLINE
    reason: str = ""


class TransitionPolicies:
    """Legal state transition matrix defining allowed state changes."""

    _ALLOWED: Dict[KernelState, Set[KernelState]] = {
        KernelState.OFFLINE: {KernelState.BOOTING, KernelState.PANIC},
        KernelState.BOOTING: {KernelState.INITIALIZING, KernelState.RECOVERY, KernelState.PANIC, KernelState.SHUTTING_DOWN},
        KernelState.INITIALIZING: {KernelState.READY, KernelState.DEGRADED, KernelState.RECOVERY, KernelState.PANIC, KernelState.SHUTTING_DOWN},
        KernelState.READY: {KernelState.BUSY, KernelState.IDLE, KernelState.DEGRADED, KernelState.MAINTENANCE, KernelState.UPDATING, KernelState.SHUTTING_DOWN, KernelState.PANIC},
        KernelState.BUSY: {KernelState.READY, KernelState.IDLE, KernelState.DEGRADED, KernelState.PANIC, KernelState.SHUTTING_DOWN},
        KernelState.IDLE: {KernelState.BUSY, KernelState.READY, KernelState.MAINTENANCE, KernelState.UPDATING, KernelState.SHUTTING_DOWN, KernelState.PANIC},
        KernelState.DEGRADED: {KernelState.READY, KernelState.RECOVERY, KernelState.MAINTENANCE, KernelState.SHUTTING_DOWN, KernelState.PANIC},
        KernelState.MAINTENANCE: {KernelState.READY, KernelState.IDLE, KernelState.SHUTTING_DOWN, KernelState.PANIC},
        KernelState.RECOVERY: {KernelState.INITIALIZING, KernelState.READY, KernelState.DEGRADED, KernelState.PANIC, KernelState.SHUTTING_DOWN},
        KernelState.UPDATING: {KernelState.INITIALIZING, KernelState.READY, KernelState.PANIC, KernelState.SHUTTING_DOWN},
        KernelState.SHUTTING_DOWN: {KernelState.OFFLINE, KernelState.PANIC},
        KernelState.PANIC: {KernelState.OFFLINE, KernelState.RECOVERY},
    }

    @classmethod
    def is_allowed(cls, from_state: KernelState, to_state: KernelState) -> bool:
        return to_state in cls._ALLOWED.get(from_state, set())


class StateValidation:
    """Validates state preconditions before executing state transitions."""

    @staticmethod
    def validate_transition(from_state: KernelState, to_state: KernelState) -> bool:
        if not TransitionPolicies.is_allowed(from_state, to_state):
            logger.warning(f"Illegal kernel state transition attempted: {from_state.value} -> {to_state.value}")
            return False
        return True


class StateObservers:
    """Observers notified synchronously or asynchronously on state transitions."""

    def __init__(self):
        self._listeners: List[Callable[[KernelState, KernelState], None]] = []

    def register(self, listener: Callable[[KernelState, KernelState], None]) -> None:
        self._listeners.append(listener)

    def notify(self, prev: KernelState, curr: KernelState) -> None:
        for listener in self._listeners:
            try:
                listener(prev, curr)
            except Exception as e:
                logger.error(f"StateObserver callback error: {e}")


class StateTransitionManager:
    """Drives validated state transitions and publishes KernelEvents."""

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.event_bus = event_bus or default_event_bus
        self.observers = StateObservers()

    def execute_transition(self, current: KernelState, target: KernelState, reason: str = "") -> Optional[KernelState]:
        if not StateValidation.validate_transition(current, target):
            return None

        logger.info(f"Kernel State Transition: {current.value} -> {target.value} (Reason: '{reason}')")
        self.observers.notify(current, target)
        self.event_bus.publish(KernelEvents(previous_state=current, current_state=target, reason=reason))
        return target


class KernelStateMachine:
    """Formal Kernel State Machine maintaining current KernelState."""

    def __init__(self, event_bus: Optional[EventBus] = None):
        self._state: KernelState = KernelState.OFFLINE
        self.transition_manager = StateTransitionManager(event_bus=event_bus)
        self._history: List[Dict[str, Any]] = []
        self._record_state_change(KernelState.OFFLINE, KernelState.OFFLINE, "Initialization")

    @property
    def current_state(self) -> KernelState:
        return self._state

    def _record_state_change(self, prev: KernelState, curr: KernelState, reason: str) -> None:
        self._history.append({
            "from": prev.value,
            "to": curr.value,
            "reason": reason,
            "timestamp": time.time(),
        })

    def transition_to(self, target_state: KernelState, reason: str = "") -> bool:
        """Transitions kernel to target_state if valid."""
        if target_state == self._state:
            return True

        new_state = self.transition_manager.execute_transition(self._state, target_state, reason=reason)
        if new_state is not None:
            prev = self._state
            self._state = new_state
            self._record_state_change(prev, new_state, reason)
            return True
        return False

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)


class KernelStateManager:
    """Convenience manager coordinating state machine, observers, and state queries."""

    def __init__(self, fsm: Optional[KernelStateMachine] = None):
        self.fsm = fsm or KernelStateMachine()

    def set_state(self, state: KernelState, reason: str = "") -> bool:
        return self.fsm.transition_to(state, reason=reason)

    def is_ready(self) -> bool:
        return self.fsm.current_state in (KernelState.READY, KernelState.BUSY, KernelState.IDLE)
