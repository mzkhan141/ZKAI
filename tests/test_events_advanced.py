from dataclasses import dataclass, field
from zkai.core.events import EventBus, Event, Signal, Publisher, Subscriber, Trigger, Observer, on_event, EventReplay, PersistentEventLog


@dataclass
class CustomEvent(Event):
    value: int = 0


def test_publisher_subscriber():
    bus = EventBus()
    pub = Publisher(source="test_src", bus=bus)
    sub = Subscriber(bus=bus)

    received = []

    @sub.listen(CustomEvent)
    def handle_custom(event: CustomEvent):
        received.append(event)

    pub.publish(CustomEvent(value=42))
    assert len(received) == 1
    assert received[0].value == 42


def test_trigger():
    bus = EventBus()
    triggered = []

    def pred(evt: Event) -> bool:
        return isinstance(evt, Signal) and getattr(evt, "name", "") == "fire"

    def act(evt: Event) -> None:
        triggered.append(evt)

    trig = Trigger(predicate=pred, action=act, bus=bus)
    bus.publish(Signal(name="fire"))
    assert len(triggered) == 1


def test_observer_pattern():
    bus = EventBus()

    class SampleObserver(Observer):
        def __init__(self):
            self.handled = []

        @on_event(CustomEvent)
        def on_custom(self, evt: CustomEvent):
            self.handled.append(evt)

    obs = SampleObserver()
    obs.register_observers(bus)

    bus.publish(CustomEvent(value=100))
    assert len(obs.handled) == 1
