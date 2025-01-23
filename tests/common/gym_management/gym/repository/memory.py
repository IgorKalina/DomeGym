import uuid
from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from tests.common.gym_management.common.repository_state import RepositorySharedState


class GymMemoryRepository(GymRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__gyms: List[GymDB] = self.__shared_state.gyms

    async def get_by_id(self, gym_id: uuid.UUID, subscription_id: uuid.UUID) -> GymDB | None:
        for gym in self.__gyms:
            if gym.id == gym_id and gym.subscription_id == subscription_id:
                return self.__create_gym_dto(gym)
        return None

    async def create(self, gym: GymDB) -> None:
        self.__gyms.append(gym)

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[GymDB]:
        return [self.__create_gym_dto(gym) for gym in self.__gyms if gym.subscription_id == subscription_id]

    async def delete(self, gym: GymDB) -> None:
        self.__gyms.remove(gym)

    def __create_gym_dto(self, gym: GymDB) -> GymDB:
        return self.__add_room_ids(gym)

    def __add_room_ids(self, gym: GymDB) -> GymDB:
        gym.room_ids = [room.id for room in self.__shared_state.rooms if room.gym_id == gym.id]
        return gym
