import uuid
from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from tests.common.gym_management.common.repository_state import RepositorySharedState


class RoomMemoryRepository(RoomRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__rooms: List[RoomDB] = self.__shared_state.rooms

    async def get_by_id(self, room_id: uuid.UUID) -> RoomDB | None:
        return next((room for room in self.__rooms if room.id == room_id), None)

    async def create(self, room: RoomDB) -> None:
        self.__rooms.append(room)

    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[GymDB]:
        return [room for room in self.__rooms if room.gym_id == gym_id]

    async def delete(self, room: RoomDB) -> None:
        self.__rooms.remove(room)
