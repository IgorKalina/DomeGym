import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.dto.repository import GymDB


class GymMemoryRepository(GymRepository):
    def __init__(self) -> None:
        self.__gyms: List[GymDB] = []

    async def get_by_id(self, gym_id: uuid.UUID) -> GymDB | None:
        return next((gym for gym in self.__gyms if gym.id == gym_id), None)

    async def create(self, gym: GymDB) -> None:
        self.__gyms.append(gym)

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[GymDB]:
        return [gym for gym in self.__gyms if gym.subscription_id == subscription_id]
