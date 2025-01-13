import uuid

from src.gym_management.domain.gym.aggregate_root import Gym
from tests.common.gym_management import constants


class GymFactory:
    @staticmethod
    def create_gym(
        id: uuid.UUID = constants.gym.GYM_ID,
        name: str = constants.gym.NAME,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
        max_rooms: int = constants.subscription.MAX_ROOMS_FREE_TIER,
    ) -> Gym:
        return Gym(id=id, name=name, subscription_id=subscription_id, max_rooms=max_rooms)
