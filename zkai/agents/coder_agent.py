"""CoderAgent specialized in software development and debugging."""

from zkai.coding.generator import CodeGenerator


class CoderAgent:
    """Specialized Agent for software generation, linting, and execution."""

    def __init__(self):
        self.code_gen = CodeGenerator()

    def write_code(self, specification: str) -> str:
        return self.code_gen.generate_code(specification)
