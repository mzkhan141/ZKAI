"""Streaming Token Generators and Callback interfaces."""

from typing import Callable, Generator


class StreamCallback:
    """Callback for processing streamed output tokens."""

    def __init__(self, callback_fn: Callable[[str], None]):
        self.callback_fn = callback_fn

    def on_token(self, token: str) -> None:
        self.callback_fn(token)


class StreamingGenerator:
    """Helper wrapper for streaming token yielders."""

    @staticmethod
    def stream_to_console(token_generator: Generator[str, None, None]) -> str:
        full_text = []
        for token in token_generator:
            print(token, end="", flush=True)
            full_text.append(token)
        print()
        return "".join(full_text)
