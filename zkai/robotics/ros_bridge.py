"""ROS1 and ROS2 bridge integration abstraction."""

from typing import Any, Callable, Dict
from zkai.core.logger import get_logger

logger = get_logger("robotics.ros")


class ROSBridge:
    """Robot Operating System (ROS1/ROS2) pub/sub message bridge."""

    def __init__(self, master_uri: str = "http://localhost:11311"):
        self.master_uri = master_uri
        self.subscriptions: Dict[str, Callable[[Any], None]] = {}

    def publish(self, topic: str, message: Any) -> None:
        logger.info(f"ROS Publish [{topic}]: {message}")

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        self.subscriptions[topic] = callback
        logger.info(f"ROS Subscribed [{topic}]")
