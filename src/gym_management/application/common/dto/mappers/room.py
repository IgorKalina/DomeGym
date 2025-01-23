from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription.aggregate_root import Subscription


def db_to_domain(room: RoomDB, subscription: Subscription) -> Room:
    return Room(
        id=room.id,
        name=room.name,
        gym_id=room.gym_id,
        max_daily_sessions=subscription.max_daily_sessions,
        created_at=room.created_at,
    )


def domain_to_db(room: Room, gym: Gym) -> RoomDB:
    return RoomDB(
        id=room.id, name=room.name, gym_id=room.gym_id, subscription_id=gym.subscription_id, created_at=room.created_at
    )
