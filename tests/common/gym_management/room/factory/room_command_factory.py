import uuid

from src.gym_management.application.room.commands.create_room import CreateRoom
from tests.common.gym_management.common import constants


class RoomCommandFactory:
    @staticmethod
    def create_create_room_command(
        name: str | None = constants.room.NAME,
        gym_id: uuid.UUID = constants.gym.GYM_ID,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
    ) -> CreateRoom:
        return CreateRoom(name=name, gym_id=gym_id, subscription_id=subscription_id)
