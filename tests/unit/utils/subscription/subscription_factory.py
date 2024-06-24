import uuid
from typing import List, Optional

from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType


class SubscriptionFactory:
    @staticmethod
    def create_subscription(
        subscription_type: SubscriptionType = SubscriptionType.FREE,
        admin_id: Optional[uuid.UUID] = None,
        gym_ids: Optional[List[uuid.UUID]] = None,  # todo: add this to constants
    ) -> Subscription:
        if admin_id is None:
            admin_id = uuid.uuid4()
        if gym_ids is None:
            gym_ids = []
        return Subscription(subscription_type=subscription_type, admin_id=admin_id, gym_ids=gym_ids)
