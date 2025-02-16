import uuid
from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.room.exceptions import RoomDoesNotExistError
from tests.common.gym_management.common.repository_state import RepositorySharedState
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.subscription.repository.memory import SubscriptionMemoryRepository


class RoomMemoryRepository(RoomRepository):
    def __init__(
        self,
        shared_state: RepositorySharedState,
        subscription_repository: SubscriptionMemoryRepository,
        gym_repository: GymMemoryRepository,
    ) -> None:
        self.__shared_state = shared_state
        self.__rooms: List[RoomDB] = self.__shared_state.rooms
        self.__subscription_repository: SubscriptionMemoryRepository = subscription_repository
        self.__gym_repository: GymMemoryRepository = gym_repository

    async def get(self, room_id: uuid.UUID) -> Room:
        room: Room | None = await self.get_or_none(room_id)
        if room is None:
            raise RoomDoesNotExistError()
        return room

    async def get_or_none(self, room_id: uuid.UUID) -> Room | None:
        for room in self.__rooms:
            if room.id == room_id:
                await self.__subscription_repository.get(room.subscription_id)
                await self.__gym_repository.get(room.gym_id)
                return room
        return None

    async def create(self, room: RoomDB) -> None:
        self.__rooms.append(room)

    async def get_by_gym_id(self, gym_id: uuid.UUID) -> List[GymDB]:
        gym = await self.__gym_repository.get(gym_id)
        await self.__subscription_repository.get(gym.subscription_id)
        return [room for room in self.__rooms if room.gym_id == gym_id]

    async def delete(self, room: RoomDB) -> None:
        self.__rooms.remove(room)
