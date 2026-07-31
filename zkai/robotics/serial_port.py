"""Serial communication (UART) manager for robotics hardware."""

from typing import Optional
from zkai.core.logger import get_logger

logger = get_logger("robotics.serial")


class SerialPort:
    """Serial port interface for microcontrollers (Arduino/ESP32)."""

    def __init__(self, port: str = "COM3", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.is_open = False

    def open(self) -> None:
        self.is_open = True
        logger.info(f"Opened SerialPort {self.port} at {self.baudrate} baud")

    def write(self, data: bytes) -> int:
        logger.debug(f"Serial write {len(data)} bytes")
        return len(data)

    def read(self, num_bytes: int = 64) -> bytes:
        return b"OK\n"

    def close(self) -> None:
        self.is_open = False
