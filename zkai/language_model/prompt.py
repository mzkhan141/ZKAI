"""Prompt, PromptTemplate, PromptBuilder, and SystemPrompt utilities."""

from typing import Any, Dict


class SystemPrompt:
    DEFAULT = "You are ZKAI, an autonomous, production-grade AI Operating System."


class PromptTemplate:
    """Template for formatting prompt strings with dynamic variables."""

    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)


class PromptBuilder:
    """Builder pattern for constructing complex structured prompts."""

    def __init__(self):
        self.parts = []

    def add_system(self, text: str) -> "PromptBuilder":
        self.parts.append(f"System: {text}")
        return self

    def add_context(self, context: str) -> "PromptBuilder":
        self.parts.append(f"Context:\n{context}")
        return self

    def add_instruction(self, instruction: str) -> "PromptBuilder":
        self.parts.append(f"Instruction:\n{instruction}")
        return self

    def build(self) -> str:
        return "\n\n".join(self.parts)
