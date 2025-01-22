from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.domain.subscription.aggregate_root import Subscription


def db_to_domain(subscription: SubscriptionDB, gyms: List[GymDB]) -> Subscription:
    return Subscription(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        gym_ids=[gym.id for gym in gyms],
        created_at=subscription.created_at,
    )


def domain_to_db(subscription: Subscription) -> SubscriptionDB:
    return SubscriptionDB(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        created_at=subscription.created_at,
    )
