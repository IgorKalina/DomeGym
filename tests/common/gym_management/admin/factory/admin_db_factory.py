import uuid

from src.gym_management.application.common.dto.repository import AdminDB
from tests.common.gym_management.common import constants


class AdminDBFactory:
    @staticmethod
    def create_admin(
        admin_id: uuid.UUID = constants.admin.ADMIN_ID,
        user_id: uuid.UUID = constants.admin.USER_ID,
        subscription_id: uuid.UUID | None = constants.subscription.SUBSCRIPTION_ID,
    ) -> AdminDB:
        return AdminDB(id=admin_id, user_id=user_id, subscription_id=subscription_id)
