from typing import List

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionsMemoryRepository(SubscriptionsRepository):
    def __init__(self) -> None:
        self._subscriptions: List[Subscription] = []

    async def create(self, subscription: Subscription) -> None:
        self._subscriptions.append(subscription)

    async def get_multi(self) -> List[Subscription]:
        return self._subscriptions.copy()
