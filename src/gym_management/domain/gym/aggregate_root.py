import uuid
from typing import List

from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.gym_management.domain.gym.exceptions import GymCannotHaveMoreRoomsThanSubscriptionAllowsError
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.room.exceptions import RoomDoesNotExistInGymError
from src.shared_kernel.domain.common.aggregate_root import AggregateRoot


class Gym(AggregateRoot):
    name: str
    subscription_id: uuid.UUID
    max_rooms: int
    room_ids: List[uuid.UUID] = []
    trainer_ids: List[uuid.UUID] = []

    def add_room(self, room: Room) -> None:
        if len(self.room_ids) >= self.max_rooms:
            raise GymCannotHaveMoreRoomsThanSubscriptionAllowsError(max_rooms=self.max_rooms)

        self.room_ids.append(room.id)
        self._create_domain_event(RoomAddedEvent(gym=self.model_copy(), room=room.model_copy()))

    def remove_room(self, room: Room) -> None:
        if room.id not in self.room_ids:
            raise RoomDoesNotExistInGymError()
        self.room_ids.remove(room.id)
        self._create_domain_event(RoomRemovedEvent(gym=self.model_copy(), room_id=room.id))

    def has_room(self, room_id: uuid.UUID) -> bool:
        return room_id in self.room_ids

    def add_trainer(self, trainer_id: uuid.UUID) -> None:
        self.trainer_ids.append(trainer_id)

    def has_trainer(self, trainer_id: uuid.UUID) -> bool:
        return trainer_id in self.trainer_ids


RoomAddedEvent.model_rebuild()
RoomRemovedEvent.model_rebuild()
