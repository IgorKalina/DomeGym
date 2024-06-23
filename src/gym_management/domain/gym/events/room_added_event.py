from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.gym_management.domain.common.event import DomainEvent
from src.gym_management.domain.room.aggregate_root import Room

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym


@dataclass
class RoomAddedEvent(DomainEvent):
    gym: "Gym"
    room: Room
