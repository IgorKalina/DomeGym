from src.gym_management.presentation.api.controllers.common.requests.base import ApiRequest


class CreateGymRequest(ApiRequest):
    name: str
