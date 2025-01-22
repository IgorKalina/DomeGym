from typing import List

from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription


def map_gym_dto_to_domain(gym: GymDB, subscription: Subscription, rooms: List[RoomDB]) -> Gym:
    return Gym(
        id=gym.id,
        name=gym.name,
        subscription_id=subscription.id,
        max_rooms=subscription.max_rooms,
        room_ids=[room.id for room in rooms],
        created_at=gym.created_at,
    )


def map_gym_domain_to_db_dto(gym: Gym) -> GymDB:
    return GymDB(id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at)
