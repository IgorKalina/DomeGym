import uuid
from typing import Optional

from src.gym_management.domain.room.aggregate_root import Room


class RoomFactory:
    @staticmethod
    def create_room(
        name: Optional[str] = None,
        gym_id: Optional[uuid.UUID] = None,
        max_daily_sessions: int = 3,  # todo: add this to constants
    ) -> Room:
        if name is None:
            name = f"room_{gym_id}"
        if gym_id is None:
            gym_id = uuid.uuid4()
        return Room(name=name, gym_id=gym_id, max_daily_sessions=max_daily_sessions)
