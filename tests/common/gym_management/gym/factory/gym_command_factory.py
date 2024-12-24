import uuid

from src.gym_management.application.gyms.commands.create_gym import CreateGym
from tests.common.gym_management import constants


class GymCommandFactory:
    @staticmethod
    def create_create_gym_command(
        name: str | None = None,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
    ) -> CreateGym:
        if name is None:
            name = f"Gym_{uuid.uuid4()}"
        return CreateGym(name=name, subscription_id=subscription_id)
