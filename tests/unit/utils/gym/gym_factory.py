import uuid
from typing import Optional

from src.gym_management.domain.gym.aggregate_root import Gym


class GymFactory:
    @staticmethod
    def create_gym(
        name: Optional[str] = None,
        subscription_id: Optional[uuid.UUID] = None,
        max_rooms: int = 3,  # todo: add this to constants
    ) -> Gym:
        if name is None:
            name = f"gym_{subscription_id}"
        if subscription_id is None:
            subscription_id = uuid.uuid4()
        return Gym(name=name, subscription_id=subscription_id, max_rooms=max_rooms)
