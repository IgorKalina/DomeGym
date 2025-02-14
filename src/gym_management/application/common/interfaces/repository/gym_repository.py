import abc
import uuid
from typing import List

from src.gym_management.domain.gym.aggregate_root import Gym


class GymRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, gym: Gym) -> None:
        pass

    @abc.abstractmethod
    async def get(self, gym_id: uuid.UUID) -> Gym:
        pass

    @abc.abstractmethod
    async def get_or_none(self, gym_id: uuid.UUID) -> Gym | None:
        pass

    @abc.abstractmethod
    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[Gym]:
        pass

    @abc.abstractmethod
    async def delete(self, gym: Gym) -> None:
        pass
