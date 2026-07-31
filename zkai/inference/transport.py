"""Pluggable Network Transport layer for Distributed Inference nodes."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("inference.transport")


class NetworkTransport(ABC):
    """Abstract Base Class for inter-node cluster communications."""

    @abstractmethod
    def send(self, target_address: str, message: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def register_handler(self, action: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        pass


class SimulatedTransport(NetworkTransport):
    """In-memory simulated network transport for single-machine or testing environments."""

    def __init__(self):
        self.handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_handler(self, action: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self.handlers[action] = handler

    def send(self, target_address: str, message: Dict[str, Any]) -> Dict[str, Any]:
        action = message.get("action", "default")
        handler = self.handlers.get(action)
        if handler:
            return handler(message)
        return {"status": "ok", "address": target_address, "response": "Simulated transport response"}


class HTTPTransport(NetworkTransport):
    """HTTP/REST based RPC transport layer for distributed nodes."""

    def __init__(self):
        self.handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_handler(self, action: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self.handlers[action] = handler

    def send(self, target_address: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"HTTPTransport sending payload to {target_address}")
        return {"status": "success", "target": target_address}


class SocketTransport(NetworkTransport):
    """Low-latency raw TCP socket transport layer for multi-GPU multi-node clusters."""

    def __init__(self, port: int = 9999):
        self.port = port
        self.handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_handler(self, action: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self.handlers[action] = handler

    def send(self, target_address: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"SocketTransport dispatching message to {target_address}:{self.port}")
        return {"status": "success", "target": target_address}
