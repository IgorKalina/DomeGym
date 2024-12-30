import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.domain.gym.aggregate_root import Gym


class GymMemoryRepository(GymRepository):
    def __init__(self) -> None:
        self.__gyms: List[Gym] = []

    async def get_by_id(self, gym_id: uuid.UUID) -> Gym | None:
        return next((gym for gym in self.__gyms if gym.id == gym_id), None)

    async def create(self, gym: Gym) -> None:
        self.__gyms.append(gym)
