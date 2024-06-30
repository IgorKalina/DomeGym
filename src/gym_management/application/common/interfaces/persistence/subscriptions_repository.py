import abc
from typing import List

from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionsRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, subscription: Subscription) -> None:
        pass

    @abc.abstractmethod
    async def get_multi(self) -> List[Subscription]:
        pass
