from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.shared_kernel.domain.common.event import DomainEvent

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.room.aggregate_root import Room


@dataclass(kw_only=True, frozen=True)
class RoomAddedEvent(DomainEvent):
    gym: "Gym"
    room: "Room"
