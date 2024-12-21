import uuid

from src.gym_management.domain.gym.aggregate_root import Gym
from tests.common.gym_management import constants


class GymFactory:
    @staticmethod
    def create_gym(
        name: str | None = None,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
        max_rooms: int = constants.subscription.MAX_ROOMS_FREE_TIER,
    ) -> Gym:
        if name is None:
            name = f"gym_{subscription_id}"
        return Gym(name=name, subscription_id=subscription_id, max_rooms=max_rooms)
