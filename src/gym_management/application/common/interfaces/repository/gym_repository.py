import abc
import uuid
from typing import List

from src.gym_management.application.gym.dto.repository import GymDB


class GymRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, gym: GymDB) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, gym_id: uuid.UUID) -> GymDB | None:
        pass

    @abc.abstractmethod
    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[GymDB]:
        pass
