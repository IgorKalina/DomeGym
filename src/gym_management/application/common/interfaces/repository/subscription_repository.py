import abc
import uuid
from typing import List

from src.gym_management.application.subscription.dto.repository import SubscriptionDB


class SubscriptionRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, subscription: SubscriptionDB) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, subscription_id: uuid.UUID) -> SubscriptionDB | None:
        pass

    @abc.abstractmethod
    async def get_by_admin_id(self, admin_id: uuid.UUID) -> SubscriptionDB | None:
        pass

    @abc.abstractmethod
    async def get_multi(self) -> List[SubscriptionDB]:
        pass

    @abc.abstractmethod
    async def update(self, subscription: SubscriptionDB) -> SubscriptionDB:
        pass
