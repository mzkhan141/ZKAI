"""Unified Robot facade combining sensors, actuators, and communication."""

from typing import Optional
from zkai.robotics.camera import RobotCamera
from zkai.robotics.gpio import GPIO
from zkai.robotics.microphone import RobotMicrophone
from zkai.robotics.ros_bridge import ROSBridge
from zkai.robotics.serial_port import SerialPort
from zkai.core.logger import get_logger

logger = get_logger("robotics.robot")


class Robot:
    """Master facade class representing an autonomous robotic agent."""

    def __init__(self, name: str = "ZKAI-Bot"):
        self.name = name
        self.camera = RobotCamera()
        self.microphone = RobotMicrophone()
        self.gpio = GPIO()
        self.serial = SerialPort()
        self.ros = ROSBridge()
        logger.info(f"Initialized Robot facade: {self.name}")
