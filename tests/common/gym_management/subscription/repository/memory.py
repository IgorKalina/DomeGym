import uuid
from typing import List

from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)


class SubscriptionMemoryRepository(SubscriptionRepository):
    def __init__(self) -> None:
        self.__subscriptions: List[SubscriptionDB] = []

    async def get_by_id(self, subscription_id: uuid.UUID) -> SubscriptionDB | None:
        return next((sub for sub in self.__subscriptions if sub.id == subscription_id), None)

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> SubscriptionDB | None:
        return next((sub for sub in self.__subscriptions if sub.admin_id == admin_id), None)

    async def create(self, subscription: SubscriptionDB) -> None:
        self.__subscriptions.append(subscription)

    async def get_multi(self) -> List[SubscriptionDB]:
        return self.__subscriptions.copy()

    async def update(self, subscription: SubscriptionDB) -> SubscriptionDB:
        updated_subscriptions = [sub for sub in self.__subscriptions if sub.id != subscription.id]
        updated_subscriptions.append(subscription)
        self.__subscriptions = updated_subscriptions
        return subscription

    async def delete(self, subscription: SubscriptionDB) -> None:
        self.__subscriptions.remove(subscription)
