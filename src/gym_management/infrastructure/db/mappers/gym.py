from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.infrastructure.db import models


def map_gym_domain_model_to_db_model(gym: Gym) -> models.Gym:
    return models.Gym(
        id=gym.id,
        name=gym.name,
        subscription_id=gym.subscription_id,
    )


def map_gym_db_model_to_domain_model(gym: models.Gym) -> Gym:
    return Gym(
        id=gym.id,
        name=gym.name,
        subscription_id=gym.subscription_id,
        max_rooms=3,
    )
