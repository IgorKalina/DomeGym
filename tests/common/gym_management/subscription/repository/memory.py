import uuid
from typing import List

from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from tests.common.gym_management.common.repository_state import RepositorySharedState


class SubscriptionMemoryRepository(SubscriptionRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__subscriptions: List[SubscriptionDB] = self.__shared_state.subscriptions

    async def get_by_id(self, subscription_id: uuid.UUID) -> SubscriptionDB | None:
        return next(
            (self.__create_subscription_dto(sub) for sub in self.__subscriptions if sub.id == subscription_id), None
        )

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> SubscriptionDB | None:
        return next(
            (self.__create_subscription_dto(sub) for sub in self.__subscriptions if sub.admin_id == admin_id), None
        )

    async def create(self, subscription: SubscriptionDB) -> None:
        self.__subscriptions.append(subscription)

    async def get_multi(self) -> List[SubscriptionDB]:
        return [self.__create_subscription_dto(sub) for sub in self.__subscriptions]

    async def update(self, subscription: SubscriptionDB) -> SubscriptionDB:
        updated_subscriptions = [sub for sub in self.__subscriptions if sub.id != subscription.id]
        updated_subscriptions.append(subscription)
        self.__subscriptions = updated_subscriptions
        return subscription

    async def delete(self, subscription: SubscriptionDB) -> None:
        self.__subscriptions = [sub for sub in self.__subscriptions if sub.id != subscription.id]

    def __create_subscription_dto(self, subscription: SubscriptionDB) -> SubscriptionDB:
        return self.__add_gym_ids(subscription)

    def __add_gym_ids(self, subscription: SubscriptionDB) -> SubscriptionDB:
        subscription.gym_ids = [gym.id for gym in self.__shared_state.gyms if gym.subscription_id == subscription.id]
        return subscription
