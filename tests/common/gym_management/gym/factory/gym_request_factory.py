from src.gym_management.presentation.api.controllers.gym.v1.requests.create_gym_request import CreateGymRequest
from tests.common.gym_management import constants


class GymRequestFactory:
    @staticmethod
    def create_create_gym_request(
        name: str = constants.gym.NAME,
    ) -> CreateGymRequest:
        return CreateGymRequest(name=name)
