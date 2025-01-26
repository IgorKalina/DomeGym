from typing import List

from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent


def db_to_domain(gym: GymDB, subscription: Subscription) -> Gym:
    return Gym(
        id=gym.id,
        name=gym.name,
        subscription_id=subscription.id,
        max_rooms=subscription.max_rooms,
        room_ids=gym.room_ids,
        created_at=gym.created_at,
    )


def gym_removed_event_to_domain(event: GymRemovedEvent, rooms: List[RoomDB]) -> Gym:
    return Gym(
        id=event.gym.id,
        name=event.gym.name,
        subscription_id=event.subscription.id,
        max_rooms=event.subscription.max_rooms,
        room_ids=[room.id for room in rooms],
    )


def domain_to_db(gym: Gym) -> GymDB:
    return GymDB(id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at)
