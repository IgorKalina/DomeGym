import abc
import uuid
from typing import List, Optional

from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionsRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, subscription: Subscription) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[Subscription]:
        pass

    @abc.abstractmethod
    async def get_multi(self) -> List[Subscription]:
        pass

    @abc.abstractmethod
    async def update(self, subscription: Subscription) -> Subscription:
        pass
