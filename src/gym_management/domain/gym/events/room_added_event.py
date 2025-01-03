from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.gym_management.domain.room.aggregate_root import Room
from src.shared_kernel.domain.event import DomainEvent

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym


@dataclass(kw_only=True)
class RoomAddedEvent(DomainEvent):
    gym: "Gym"
    room: Room
