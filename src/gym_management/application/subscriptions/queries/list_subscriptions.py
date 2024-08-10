from dataclasses import dataclass
from typing import List

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.query import Query, QueryHandler


@dataclass(frozen=True)
class ListSubscriptions(Query):
    pass


class ListSubscriptionsHandler(QueryHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, query: ListSubscriptions) -> List[Subscription]:
        subscriptions = await self._subscriptions_repository.get_multi()
        return subscriptions
