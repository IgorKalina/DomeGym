from src.gym_management.presentation.api.controllers.common.requests.base import ApiRequest


class CreateRoomRequest(ApiRequest):
    name: str
