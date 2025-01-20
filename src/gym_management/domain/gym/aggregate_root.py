import uuid
from typing import List

from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.gym_management.domain.gym.exceptions import GymCannotHaveMoreRoomsThanSubscriptionAllowsError
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.room.exceptions import RoomDoesNotExistError


class Gym(AggregateRoot):
    def __init__(
        self,
        *,
        name: str,
        subscription_id: uuid.UUID,
        max_rooms: int,
        room_ids: List[uuid.UUID],
        trainer_ids: List[uuid.UUID],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.name = name
        self.subscription_id = subscription_id

        self.__max_rooms = max_rooms
        self.__room_ids = room_ids
        self.__trainer_ids = trainer_ids

    def add_room(self, room: Room) -> None:
        if len(self.__room_ids) >= self.__max_rooms:
            raise GymCannotHaveMoreRoomsThanSubscriptionAllowsError(max_rooms=self.__max_rooms)

        self.__room_ids.append(room.id)
        self._create_domain_event(RoomAddedEvent(gym=self, room=room))

    def remove_room(self, room: Room) -> None:
        if room.id not in self.__room_ids:
            raise RoomDoesNotExistError()
        self.__room_ids.remove(room.id)
        self._create_domain_event(RoomRemovedEvent(gym=self, room_id=room.id))

    def has_room(self, room_id: uuid.UUID) -> bool:
        return room_id in self.__room_ids

    def add_trainer(self, trainer_id: uuid.UUID) -> None:
        self.__trainer_ids.append(trainer_id)

    def has_trainer(self, trainer_id: uuid.UUID) -> bool:
        return trainer_id in self.__trainer_ids
