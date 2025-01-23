import uuid

from src.gym_management.domain.room.aggregate_root import Room
from tests.common.gym_management.common import constants


class RoomFactory:
    @staticmethod
    def create_room(
        name: str | None = None,
        gym_id: uuid.UUID | None = None,
        max_daily_sessions: int = constants.subscription.MAX_SESSIONS_FREE_TIER,
    ) -> Room:
        if name is None:
            name = f"room_{gym_id}"
        if gym_id is None:
            gym_id = uuid.uuid4()
        return Room(name=name, gym_id=gym_id, max_daily_sessions=max_daily_sessions)
