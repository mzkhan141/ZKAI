"""Unit tests for Robotics subsystem."""

import pytest
from zkai.robotics import GPIO, Drone, FlightPlan, PinMode, Robot, ROSBridge, SerialPort, USBManager


def test_gpio():
    gpio = GPIO()
    gpio.setup(18, PinMode.OUTPUT)
    gpio.write(18, 1)
    assert gpio.read(18) == 1


def test_robot_facade():
    robot = Robot("TestBot")
    assert robot.name == "TestBot"
    assert robot.camera is not None
    assert robot.gpio is not None
