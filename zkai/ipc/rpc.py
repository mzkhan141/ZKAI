"""RPC Server, Client, and Remote Procedure Calls for ZKAI IPC."""

import asyncio
from typing import Any, Callable, Dict, Optional
import uuid
from zkai.ipc.bus import IPCMessage, SystemMessageBus
from zkai.core.logger import get_logger

logger = get_logger("ipc.rpc")


class RPCServer:
    """Server exporting callable methods for RPC execution over SystemMessageBus."""

    def __init__(self, service_name: str, bus: Optional[SystemMessageBus] = None):
        self.service_name = service_name
        self.bus = bus or SystemMessageBus()
        self.methods: Dict[str, Callable[..., Any]] = {}
        self.bus.subscribe_topic(f"rpc_request_{service_name}", self._handle_request)

    def register_method(self, name: str, fn: Callable[..., Any]) -> None:
        self.methods[name] = fn
        logger.info(f"RPCServer '{self.service_name}' registered method: '{name}'")

    def _handle_request(self, msg: IPCMessage) -> None:
        payload = msg.payload or {}
        method_name = payload.get("method")
        req_id = payload.get("request_id")
        args = payload.get("args", [])
        kwargs = payload.get("kwargs", {})

        if method_name in self.methods:
            try:
                result = self.methods[method_name](*args, **kwargs)
                response = IPCMessage(
                    topic=f"rpc_response_{req_id}",
                    sender_id=self.service_name,
                    recipient_id=msg.sender_id,
                    payload={"status": "success", "result": result, "request_id": req_id},
                )
            except Exception as e:
                response = IPCMessage(
                    topic=f"rpc_response_{req_id}",
                    sender_id=self.service_name,
                    recipient_id=msg.sender_id,
                    payload={"status": "error", "error": str(e), "request_id": req_id},
                )
            self.bus.publish_message(response)


class RPCClient:
    """Client issuing remote procedure calls to RPCServer endpoints."""

    def __init__(self, client_id: str = "rpc_client", bus: Optional[SystemMessageBus] = None):
        self.client_id = client_id
        self.bus = bus or SystemMessageBus()
        self._responses: Dict[str, Any] = {}

    def call(self, service_name: str, method: str, *args: Any, **kwargs: Any) -> Any:
        req_id = str(uuid.uuid4())
        topic = f"rpc_response_{req_id}"

        def _on_res(msg: IPCMessage):
            self._responses[req_id] = msg.payload

        self.bus.subscribe_topic(topic, _on_res)

        req_msg = IPCMessage(
            topic=f"rpc_request_{service_name}",
            sender_id=self.client_id,
            recipient_id=service_name,
            payload={"method": method, "request_id": req_id, "args": args, "kwargs": kwargs},
        )
        self.bus.publish_message(req_msg)
        res = self._responses.get(req_id, {"status": "success", "result": None})
        return res.get("result")


class RemoteProcedureCall:
    """Decorator wrapping local methods as RPC proxies."""

    def __init__(self, client: RPCClient, service_name: str, method_name: str):
        self.client = client
        self.service_name = service_name
        self.method_name = method_name

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.client.call(self.service_name, self.method_name, *args, **kwargs)
