import abc
import uuid
from typing import List

from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, subscription: Subscription) -> None:
        pass

    @abc.abstractmethod
    async def get(self, subscription_id: uuid.UUID) -> Subscription:
        pass

    @abc.abstractmethod
    async def get_or_none(self, subscription_id: uuid.UUID) -> Subscription | None:
        pass

    @abc.abstractmethod
    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Subscription:
        pass

    @abc.abstractmethod
    async def list(self) -> List[Subscription]:
        pass

    @abc.abstractmethod
    async def update(self, subscription: Subscription) -> Subscription:
        pass

    @abc.abstractmethod
    async def delete(self, subscription: Subscription) -> None:
        pass
