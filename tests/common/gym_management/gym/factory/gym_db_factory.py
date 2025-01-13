import uuid

from src.gym_management.application.gym.dto.repository import GymDB
from tests.common.gym_management import constants


class GymDBFactory:
    @staticmethod
    def create_gym(
        id: uuid.UUID = constants.gym.GYM_ID,
        name: str | None = constants.gym.NAME,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
    ) -> GymDB:
        return GymDB(id=id, name=name, subscription_id=subscription_id)
