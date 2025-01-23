from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription


def db_to_domain(gym: GymDB, subscription: Subscription) -> Gym:
    return Gym(
        id=gym.id,
        name=gym.name,
        subscription_id=subscription.id,
        max_rooms=subscription.max_rooms,
        room_ids=gym.room_ids,
        created_at=gym.created_at,
    )


def domain_to_db(gym: Gym) -> GymDB:
    return GymDB(id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at)
