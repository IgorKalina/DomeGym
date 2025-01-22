import abc
import uuid
from typing import List

from src.gym_management.application.common.dto.repository.room import RoomDB


class RoomRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, room: RoomDB) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, room_id: uuid.UUID) -> RoomDB | None:
        pass

    @abc.abstractmethod
    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[RoomDB]:
        pass

    @abc.abstractmethod
    async def delete(self, room: RoomDB) -> None:
        pass
