import uuid
from typing import List

from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from tests.common.gym_management.common.repository_state import RepositorySharedState


class SubscriptionMemoryRepository(SubscriptionRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__subscriptions: List[Subscription] = self.__shared_state.subscriptions

    async def get(self, subscription_id: uuid.UUID) -> Subscription:
        for sub in self.__subscriptions:
            if sub.id == subscription_id:
                return sub
        raise SubscriptionDoesNotExistError()

    async def get_or_none(self, subscription_id: uuid.UUID) -> Subscription | None:
        return next((sub for sub in self.__subscriptions if sub.id == subscription_id), None)

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Subscription:
        for sub in self.__subscriptions:
            if sub.admin_id == admin_id:
                return sub
        raise SubscriptionDoesNotExistError()

    async def create(self, subscription: Subscription) -> None:
        self.__subscriptions.append(subscription)

    async def get_multi(self) -> List[Subscription]:
        return list(self.__subscriptions)

    async def update(self, subscription: Subscription) -> Subscription:
        updated_subscriptions = [sub for sub in self.__subscriptions if sub.id != subscription.id]
        updated_subscriptions.append(subscription)
        self.__subscriptions = updated_subscriptions
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        self.__subscriptions = [sub for sub in self.__subscriptions if sub.id != subscription.id]
