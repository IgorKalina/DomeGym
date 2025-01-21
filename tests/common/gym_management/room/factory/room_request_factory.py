from src.gym_management.presentation.api.controllers.room.v1.requests.create_gym_request import CreateRoomRequest
from tests.common.gym_management import constants


class RoomRequestFactory:
    @staticmethod
    def create_create_room_request(
        name: str = constants.room.NAME,
    ) -> CreateRoomRequest:
        return CreateRoomRequest(name=name)
