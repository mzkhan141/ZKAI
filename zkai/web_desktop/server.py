"""Web Desktop Server providing HTML/JS UI dashboard for ZKAI AI Operating System."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Any, Dict, List
import json
from zkai.core.logger import get_logger

logger = get_logger("web_desktop")

app = FastAPI(title="ZKAI Web Desktop", version="1.0.0")

HTML_DASHBOARD = """<!DOCTYPE html>
<html>
<head>
    <title>ZKAI — AI Operating System Desktop</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; }
        header { background: #1e293b; padding: 12px 24px; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        h1 { margin: 0; font-size: 18px; font-weight: 600; color: #38bdf8; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; padding: 20px; }
        .panel { background: #1e293b; border-radius: 8px; border: 1px solid #334155; padding: 16px; min-height: 200px; }
        .panel h2 { margin-top: 0; font-size: 14px; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.05em; }
        .status-badge { background: #10b981; color: #022c22; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; }
    </style>
</head>
<body>
    <header>
        <h1>ZKAI AI Operating System</h1>
        <span class="status-badge">KERNEL RUNNING</span>
    </header>
    <div class="grid">
        <div class="panel"><h2>1. Conversation Center</h2><div id="chat-out">System Ready.</div></div>
        <div class="panel"><h2>2. Knowledge Graph Viewer</h2><div>Nodes: 124, Edges: 341</div></div>
        <div class="panel"><h2>3. Memory Timeline</h2><div>Consolidated short-term & long-term stores.</div></div>
        <div class="panel"><h2>4. Workflow Monitor</h2><div>Active DAGs: 0</div></div>
        <div class="panel"><h2>5. Running Agents</h2><div>Coordinator, CoderAgent, ResearchAgent</div></div>
        <div class="panel"><h2>6. Task Queue</h2><div>Pending tasks: 0</div></div>
        <div class="panel"><h2>7. Browser Panel</h2><div>Headless Browser Engine Standby</div></div>
        <div class="panel"><h2>8. Vision Panel</h2><div>OCR & Object Detection Ready</div></div>
        <div class="panel"><h2>9. Voice Panel</h2><div>Speech STT/TTS Pipeline Online</div></div>
        <div class="panel"><h2>10. Developer Console</h2><div>ZKShell Interactive Console</div></div>
        <div class="panel"><h2>11. System Notifications</h2><div>Kernel initialized successfully.</div></div>
    </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def get_dashboard() -> str:
    return HTML_DASHBOARD


@app.get("/api/status")
def get_status() -> Dict[str, Any]:
    return {"status": "ok", "kernel": "running", "panels": 11}


class WebDesktopServer:
    """Server manager running Web Desktop dashboard."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8900):
        self.host = host
        self.port = port

    def run(self) -> None:
        import uvicorn
        logger.info(f"Launching ZKAI Web Desktop Dashboard at http://{self.host}:{self.port}")
        uvicorn.run(app, host=self.host, port=self.port)
