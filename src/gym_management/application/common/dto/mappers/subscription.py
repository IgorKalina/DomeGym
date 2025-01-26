from typing import List

from src.gym_management.application.common.dto.repository import GymDB
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.subscription.aggregate_root import Subscription


def db_to_domain(subscription: SubscriptionDB) -> Subscription:
    return Subscription(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        gym_ids=subscription.gym_ids,
        created_at=subscription.created_at,
    )


def subscription_unset_event_to_domain(event: SubscriptionUnsetEvent, gyms: List[GymDB]) -> Subscription:
    return Subscription(
        id=event.subscription.id,
        type=event.subscription.type,
        admin_id=event.subscription.admin_id,
        gym_ids=[gym.id for gym in gyms],
    )


def domain_to_db(subscription: Subscription) -> SubscriptionDB:
    return SubscriptionDB(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        created_at=subscription.created_at,
    )
