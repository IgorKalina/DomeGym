import abc
import uuid
from typing import List

from src.gym_management.domain.room.aggregate_root import Room


class RoomRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, room: Room) -> None:
        pass

    @abc.abstractmethod
    async def get(self, room_id: uuid.UUID) -> Room:
        pass

    @abc.abstractmethod
    async def get_or_none(self, room_id: uuid.UUID) -> Room | None:
        pass

    @abc.abstractmethod
    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[Room]:
        pass

    @abc.abstractmethod
    async def delete(self, room: Room) -> None:
        pass
