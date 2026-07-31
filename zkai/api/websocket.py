"""WebSocketServer for real-time bidirectional token and audio streaming."""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from zkai.core.logger import get_logger

logger = get_logger("api.websocket")


class WebSocketServer:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New WebSocket client connected")

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_text(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)
