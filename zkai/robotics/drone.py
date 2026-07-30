"""Drone control abstraction and FlightPlan."""

from dataclasses import dataclass, field
from typing import List, Tuple
from zkai.core.logger import get_logger

logger = get_logger("robotics.drone")


@dataclass
class FlightPlan:
    waypoints: List[Tuple[float, float, float]] = field(default_factory=list)


class Drone:
    """Autonomous drone flight controller."""

    def takeoff(self, altitude_m: float = 2.0) -> None:
        logger.info(f"Drone taking off to target altitude {altitude_m}m")

    def land(self) -> None:
        logger.info("Drone landing")

    def fly_path(self, plan: FlightPlan) -> None:
        logger.info(f"Flying waypoint trajectory: {len(plan.waypoints)} waypoints")
