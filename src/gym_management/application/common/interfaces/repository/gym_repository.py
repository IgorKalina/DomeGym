import abc
import uuid
from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB


class GymRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, gym: GymDB) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, gym_id: uuid.UUID, subscription_id: uuid.UUID) -> GymDB | None:
        pass

    @abc.abstractmethod
    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[GymDB]:
        pass

    @abc.abstractmethod
    async def delete(self, gym: GymDB) -> None:
        pass
