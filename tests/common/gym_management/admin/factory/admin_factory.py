import uuid

from src.gym_management.domain.admin.aggregate_root import Admin
from tests.common.gym_management.common import constants


class AdminFactory:
    @staticmethod
    def create_admin(
        id: uuid.UUID = constants.admin.ADMIN_ID,
        user_id: uuid.UUID = constants.admin.USER_ID,
        subscription_id: uuid.UUID | None = constants.subscription.SUBSCRIPTION_ID,
    ) -> Admin:
        return Admin(id=id, user_id=user_id, subscription_id=subscription_id)
