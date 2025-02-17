import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.exceptions import GymAlreadyExistsError, GymDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from tests.common.gym_management.common.repository_state import RepositorySharedState


class GymMemoryRepository(GymRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__gyms: List[Gym] = self.__shared_state.gyms

    async def get(self, gym_id: uuid.UUID) -> Gym:
        gym: Gym | None = await self.get_or_none(gym_id)
        if gym is None:
            raise GymDoesNotExistError(gym_id=gym_id)
        return gym

    async def get_or_none(self, gym_id: uuid.UUID) -> Gym | None:
        for gym in self.__gyms:
            if gym.id == gym_id:
                return gym
        return None

    async def create(self, gym: Gym) -> None:
        existing_gym: Gym | None = await self.get_or_none(gym.id)
        if existing_gym is not None:
            raise GymAlreadyExistsError(gym_id=gym.id)
        self.__gyms.append(gym)

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[Gym]:
        return [gym for gym in self.__gyms if gym.subscription_id == subscription_id]

    async def update(self, gym: Gym) -> Gym:
        updated_gyms = [existing_gym for existing_gym in self.__gyms if existing_gym.id != gym.id]
        updated_gyms.append(gym)
        self.__gyms = updated_gyms
        return gym

    async def delete(self, gym: Gym) -> None:
        await self.get(gym.id)
        self.__gyms.remove(gym)
