import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.room.exceptions import RoomDoesNotExistInGymError
from tests.common.gym_management.common.repository_state_memory import RepositorySharedState


class RoomMemoryRepository(RoomRepository):
    def __init__(
        self,
        shared_state: RepositorySharedState,
    ) -> None:
        self.__shared_state = shared_state
        self.__rooms: List[Room] = self.__shared_state.rooms

    async def get(self, room_id: uuid.UUID) -> Room:
        room: Room | None = await self.get_or_none(room_id)
        if room is None:
            raise RoomDoesNotExistInGymError()
        return room

    async def get_or_none(self, room_id: uuid.UUID) -> Room | None:
        for room in self.__rooms:
            if room.id == room_id:
                return room
        return None

    async def create(self, room: Room) -> None:
        self.__rooms.append(room)

    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[Room]:
        return [room for room in self.__rooms if room.gym_id == gym_id]

    async def delete(self, room_id: uuid.UUID) -> None:
        room = await self.get(room_id)
        self.__rooms.remove(room)
