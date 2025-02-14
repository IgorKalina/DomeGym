from typing import List

from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription


def subscription_unset_event_to_domain(event: SubscriptionUnsetEvent, gyms: List[Gym]) -> Subscription:
    return Subscription(
        id=event.subscription.id,
        type=event.subscription.type,
        admin_id=event.subscription.admin_id,
        gym_ids=[gym.id for gym in gyms],
    )
