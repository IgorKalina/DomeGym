import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.shared_kernel.domain.event import DomainEvent

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym


@dataclass
class RoomRemovedEvent(DomainEvent):
    gym: "Gym"
    room_id: uuid.UUID
