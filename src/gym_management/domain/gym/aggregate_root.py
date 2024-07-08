import uuid
from typing import List, Optional

from src.common.error_or import ErrorOr, ErrorResult, OkResult, Result
from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.errors import GymCannotHaveMoreRoomsThanSubscriptionAllows, RoomDoesNotExist
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.gym_management.domain.room.aggregate_root import Room


class Gym(AggregateRoot):
    def __init__(
        self,
        *,
        name: str,
        subscription_id: uuid.UUID,
        max_rooms: int,
        room_ids: Optional[List[uuid.UUID]] = None,
        trainer_ids: Optional[List[uuid.UUID]] = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.subscription_id = subscription_id

        self._max_rooms = max_rooms
        self._room_ids = room_ids or []
        self._trainer_ids = trainer_ids or []

    def add_room(self, room: Room) -> ErrorOr[Result]:
        if len(self._room_ids) >= self._max_rooms:
            return ErrorResult(GymCannotHaveMoreRoomsThanSubscriptionAllows())

        self._room_ids.append(room.id)
        self._create_domain_event(RoomAddedEvent(gym=self, room=room))
        return OkResult(Result.created())

    def remove_room(self, room: Room) -> ErrorOr[Result]:
        if room.id not in self._room_ids:
            return ErrorResult(RoomDoesNotExist())
        self._room_ids.remove(room.id)
        self._create_domain_event(RoomRemovedEvent(gym=self, room_id=room.id))
        return OkResult(Result.deleted())

    def has_room(self, room_id: uuid.UUID) -> bool:
        return room_id in self._room_ids

    def add_trainer(self, trainer_id: uuid.UUID) -> Result:
        self._trainer_ids.append(trainer_id)
        return Result.created()

    def has_trainer(self, trainer_id: uuid.UUID) -> bool:
        return trainer_id in self._trainer_ids
