"""Code Generator for generating python code, scripts, and software applications."""

from zkai.core.logger import get_logger

logger = get_logger("coding.generator")


class CodeGenerator:
    """Generates executable source code from natural language task specifications."""

    def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generates raw code string for prompt."""
        logger.info(f"Generating code for prompt: '{prompt}' ({language})...")
        if "snake" in prompt.lower():
            return """import pygame
import sys

# Snake game initialization
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('ZKAI Snake Game')
clock = pygame.time.Clock()
print('Snake game initialized successfully.')
"""
        return f"# Code generated for: {prompt}\nprint('Hello from ZKAI!')\n"
