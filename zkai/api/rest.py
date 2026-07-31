"""FastAPI REST API Server for ZKAI AI Operating System."""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Any, Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("api.rest")

app = FastAPI(title="ZKAI REST API", version="1.0.0")


class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    status: str = "success"


@app.get("/")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "system": "ZKAI"}


@app.post("/v1/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest) -> ChatResponse:
    logger.info(f"REST API Chat request received: '{req.message[:30]}...'")
    return ChatResponse(response=f"ZKAI REST API response to '{req.message}'")


class RESTServer:
    """REST API Server launcher."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port

    def run(self) -> None:
        import uvicorn
        uvicorn.run(app, host=self.host, port=self.port)
