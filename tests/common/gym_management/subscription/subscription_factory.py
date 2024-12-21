import uuid
from typing import List

from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management import constants


class SubscriptionFactory:
    @staticmethod
    def create_subscription(
        subscription_type: SubscriptionType = constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        admin_id: uuid.UUID = constants.admin.ADMIN_ID,
        gym_ids: List[uuid.UUID] | None = None,
    ) -> Subscription:
        if gym_ids is None:
            gym_ids = []
        return Subscription(subscription_type=subscription_type, admin_id=admin_id, gym_ids=gym_ids)
