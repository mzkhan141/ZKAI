"""ChatModel, Message, Conversation history, and Role abstractions."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from zkai.core.types import Role
from zkai.language_model.llm import LanguageModel, LLM


@dataclass
class Message:
    """Represents a single chat message turn."""
    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Conversation:
    """Manages chat conversation turn history and prompt compilation."""

    def __init__(self, system_prompt: str = "You are ZKAI, a production-grade AI operating system and assistant."):
        self.system_prompt = system_prompt
        self.messages: List[Message] = []
        if system_prompt:
            self.messages.append(Message(role=Role.SYSTEM, content=system_prompt))

    def add_user_message(self, content: str) -> Message:
        msg = Message(role=Role.USER, content=content)
        self.messages.append(msg)
        return msg

    def add_assistant_message(self, content: str) -> Message:
        msg = Message(role=Role.ASSISTANT, content=content)
        self.messages.append(msg)
        return msg

    def compile_prompt(self) -> str:
        """Compiles messages into a unified prompt string format."""
        formatted = []
        for msg in self.messages:
            formatted.append(f"<|im_start|>{msg.role.value}\n{msg.content}<|im_end|>")
        formatted.append("<|im_start|>assistant\n")
        return "\n".join(formatted)


class ChatModel:
    """Interactive Chat Interface powered by ZKAI Language Models."""

    def __init__(self, model: Optional[LLM] = None):
        self.model = model or LanguageModel()
        self.conversation = Conversation()

    def chat(self, user_input: str) -> str:
        """Processes user input, updates conversation history, and generates response."""
        self.conversation.add_user_message(user_input)
        prompt = self.conversation.compile_prompt()
        response_text = self.model.generate(prompt)
        self.conversation.add_assistant_message(response_text)
        return response_text
