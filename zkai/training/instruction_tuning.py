"""InstructionTuner for formatting prompt-response pairs using standard template formats."""

from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("training.instruction_tuning")


class InstructionTuner:
    """Formats raw instruction data into Alpaca, ShareGPT, or custom formatted chat prompts."""

    ALPACA_TEMPLATE = (
        "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n"
        "### Input:\n{input}\n\n"
        "### Response:\n{output}"
    )

    ALPACA_NO_INPUT_TEMPLATE = (
        "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n"
        "### Response:\n{output}"
    )

    def __init__(self, template_type: str = "alpaca"):
        self.template_type = template_type

    def format_sample(self, instruction: str, output: str, input_text: str = "") -> str:
        """Formats a single instruction example into training target text."""
        if self.template_type == "alpaca":
            if input_text.strip():
                return self.ALPACA_TEMPLATE.format(instruction=instruction, input=input_text, output=output)
            return self.ALPACA_NO_INPUT_TEMPLATE.format(instruction=instruction, output=output)
        elif self.template_type == "chat":
            return f"User: {instruction}\nAssistant: {output}"
        else:
            return f"Instruction: {instruction}\nOutput: {output}"

    def format_dataset(self, samples: List[Dict[str, str]]) -> List[str]:
        """Formats a list of instruction dictionary records."""
        formatted = []
        for sample in samples:
            inst = sample.get("instruction") or sample.get("prompt") or ""
            out = sample.get("output") or sample.get("response") or ""
            inp = sample.get("input") or ""
            formatted.append(self.format_sample(inst, out, inp))
        return formatted
