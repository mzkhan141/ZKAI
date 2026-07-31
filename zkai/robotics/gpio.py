"""GPIO pin control abstraction for microcontrollers and single-board computers."""

from enum import Enum
from typing import Dict
from zkai.core.logger import get_logger

logger = get_logger("robotics.gpio")


class PinMode(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    PWM = "pwm"


class GPIO:
    """General Purpose Input/Output abstraction with virtual/RPi.GPIO fallback."""

    def __init__(self):
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_states: Dict[int, int] = {}

    def setup(self, pin: int, mode: PinMode) -> None:
        self.pin_modes[pin] = mode
        logger.info(f"GPIO pin {pin} setup as {mode.value}")

    def write(self, pin: int, value: int) -> None:
        self.pin_states[pin] = value
        logger.debug(f"GPIO pin {pin} write -> {value}")

    def read(self, pin: int) -> int:
        return self.pin_states.get(pin, 0)
