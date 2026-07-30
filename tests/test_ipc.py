"""Tests for Interprocess Communication, RPC, and Channels."""

import pytest
from zkai.ipc.bus import SystemMessageBus, IPCMessage
from zkai.ipc.rpc import RPCServer, RPCClient
from zkai.ipc.channels import SharedMemoryChannel, BroadcastChannel
from zkai.ipc.discovery import ServiceDiscovery


def test_system_message_bus():
    bus = SystemMessageBus()
    received = []

    def handler(msg: IPCMessage):
        received.append(msg)

    bus.subscribe_topic("test_topic", handler)
    bus.publish_message(IPCMessage(topic="test_topic", payload="Hello IPC"))
    assert len(received) == 1
    assert received[0].payload == "Hello IPC"


def test_rpc_server_client():
    bus = SystemMessageBus()
    server = RPCServer(service_name="math_service", bus=bus)
    server.register_method("add", lambda a, b: a + b)

    client = RPCClient(client_id="test_client", bus=bus)
    res = client.call("math_service", "add", 10, 20)
    assert res == 30


def test_shared_memory_channel():
    shm = SharedMemoryChannel(name="shm_test", size=64)
    data = b"ZKAI Shared Memory Payload"
    written = shm.write(data)
    assert written == len(data)
    read_data = shm.read(len(data))
    assert read_data == data


def test_service_discovery():
    sd = ServiceDiscovery()
    sd.register_service("inference_service", "localhost", 8080)
    ep = sd.resolve("inference_service")
    assert ep is not None
    assert ep["url"] == "http://localhost:8080"
