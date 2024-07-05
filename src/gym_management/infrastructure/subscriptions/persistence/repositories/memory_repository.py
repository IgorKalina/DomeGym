import uuid
from typing import List, Optional

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionsMemoryRepository(SubscriptionsRepository):
    def __init__(self) -> None:
        self._subscriptions: List[Subscription] = []

    async def get_by_id(self, subscription_id: uuid.UUID) -> Optional[Subscription]:
        return next((sub for sub in self._subscriptions if sub.id == subscription_id), None)

    async def create(self, subscription: Subscription) -> None:
        self._subscriptions.append(subscription)

    async def get_multi(self) -> List[Subscription]:
        return self._subscriptions.copy()

    async def update(self, subscription: Subscription) -> Subscription:
        updated_subscriptions = [sub for sub in self._subscriptions if sub.id == subscription.id]
        updated_subscriptions.append(subscription)
        self._subscriptions = updated_subscriptions
        return subscription
