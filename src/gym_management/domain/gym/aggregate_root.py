import uuid
from dataclasses import dataclass, field
from typing import List

from result import Ok, Result

from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.errors import GymErrors
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.gym_management.domain.room.aggregate_root import Room


@dataclass(kw_only=True)
class Gym(AggregateRoot):
    name: str
    subscription_id: uuid.UUID
    # todo: get to know how to make this property private while keeping it non-private in the constructor
    max_rooms: int

    _room_ids: List[uuid.UUID] = field(default_factory=list)
    _trainer_ids: List[uuid.UUID] = field(default_factory=list)

    def add_room(self, room: Room) -> Result:
        if len(self._room_ids) >= self.max_rooms:
            return GymErrors.cannot_have_more_rooms_than_subscription_allows()

        self._room_ids.append(room.id)
        self._create_domain_event(RoomAddedEvent(gym=self, room=room))
        return Ok(None)

    def remove_room(self, room: Room) -> Result:
        if room.id not in self._room_ids:
            return GymErrors.cannot_remove_not_existing_room()
        self._room_ids.remove(room.id)
        self._create_domain_event(RoomRemovedEvent(gym=self, room_id=room.id))
        return Ok(None)

    def has_room(self, room_id: uuid.UUID) -> bool:
        return room_id in self._room_ids

    def add_trainer(self, trainer_id: uuid.UUID) -> Result:
        self._trainer_ids.append(trainer_id)
        return Ok(None)

    def has_trainer(self, trainer_id: uuid.UUID) -> bool:
        return trainer_id in self._trainer_ids
