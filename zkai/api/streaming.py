"""StreamingResponse wrapper for FastAPI SSE token streams."""

from fastapi.responses import StreamingResponse
from typing import Generator


class ZKAIStreamingResponse:
    """Helper creating FastAPI StreamingResponse instances for token generation."""

    @staticmethod
    def create(generator: Generator[str, None, None]) -> StreamingResponse:
        return StreamingResponse(generator, media_type="text/event-stream")
