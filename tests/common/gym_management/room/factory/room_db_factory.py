import uuid

from src.gym_management.application.room.dto.repository import RoomDB
from tests.common.gym_management import constants


class RoomDBFactory:
    @staticmethod
    def create_room(
        id: uuid.UUID = constants.room.ROOM_ID,
        name: str | None = constants.room.NAME,
        gym_id: uuid.UUID = constants.gym.GYM_ID,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
    ) -> RoomDB:
        return RoomDB(id=id, name=name, gym_id=gym_id, subscription_id=subscription_id)
