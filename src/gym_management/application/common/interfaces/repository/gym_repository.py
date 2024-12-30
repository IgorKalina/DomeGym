import abc
import uuid

from src.gym_management.domain.gym.aggregate_root import Gym


class GymRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, gym: Gym) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, gym_id: uuid.UUID) -> Gym | None:
        pass
