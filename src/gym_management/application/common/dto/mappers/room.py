from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room


def domain_to_db(room: Room, gym: Gym) -> RoomDB:
    return RoomDB(
        id=room.id, name=room.name, gym_id=gym.id, subscription_id=gym.subscription_id, created_at=room.created_at
    )
