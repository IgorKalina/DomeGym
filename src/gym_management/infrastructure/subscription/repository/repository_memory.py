import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionMemoryRepository(SubscriptionRepository):
    def __init__(self) -> None:
        self.__subscriptions: List[Subscription] = []

    async def get_by_id(self, subscription_id: uuid.UUID) -> Subscription | None:
        return next((sub for sub in self.__subscriptions if sub.id == subscription_id), None)

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Subscription | None:
        return next((sub for sub in self.__subscriptions if sub.admin_id == admin_id), None)

    async def create(self, subscription: Subscription) -> None:
        self.__subscriptions.append(subscription)

    async def get_multi(self) -> List[Subscription]:
        return self.__subscriptions.copy()

    async def update(self, subscription: Subscription) -> Subscription:
        updated_subscriptions = [sub for sub in self.__subscriptions if sub.id != subscription.id]
        updated_subscriptions.append(subscription)
        self.__subscriptions = updated_subscriptions
        return subscription
