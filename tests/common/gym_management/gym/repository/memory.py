import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from tests.common.gym_management.common.repository_state import RepositorySharedState
from tests.common.gym_management.subscription.repository.memory import SubscriptionMemoryRepository


class GymMemoryRepository(GymRepository):
    def __init__(
        self, shared_state: RepositorySharedState, subscription_repository: SubscriptionMemoryRepository
    ) -> None:
        self.__shared_state = shared_state
        self.__gyms: List[Gym] = self.__shared_state.gyms
        self.__subscription_repository = subscription_repository

    async def get(self, gym_id: uuid.UUID) -> Gym:
        gym: Gym | None = await self.get_or_none(gym_id)
        if gym is None:
            raise GymDoesNotExistError()
        await self.__subscription_repository.get(gym.subscription_id)
        return gym

    async def get_or_none(self, gym_id: uuid.UUID) -> Gym | None:
        for gym in self.__gyms:
            if gym.id == gym_id:
                return self.__create_gym_dto(gym)
        return None

    async def create(self, gym: Gym) -> None:
        self.__gyms.append(gym)

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[Gym]:
        return [self.__create_gym_dto(gym) for gym in self.__gyms if gym.subscription_id == subscription_id]

    async def delete(self, gym: Gym) -> None:
        self.__gyms.remove(gym)

    def __create_gym_dto(self, gym: Gym) -> Gym:
        return self.__add_room_ids(gym)

    def __add_room_ids(self, gym: Gym) -> Gym:
        gym.room_ids = [room.id for room in self.__shared_state.rooms if room.gym_id == gym.id]
        return gym
