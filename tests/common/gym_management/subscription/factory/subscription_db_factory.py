import uuid
from typing import List

from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management.common import constants


class SubscriptionDBFactory:
    @staticmethod
    def create_subscription(
        id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
        type: SubscriptionType = constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        admin_id: uuid.UUID = constants.admin.ADMIN_ID,
        gym_ids: List[uuid.UUID] | None = None,
    ) -> SubscriptionDB:
        if gym_ids is None:
            gym_ids = []
        return SubscriptionDB(id=id, type=type, admin_id=admin_id, gym_ids=gym_ids)
