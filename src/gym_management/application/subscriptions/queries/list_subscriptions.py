from dataclasses import dataclass
from typing import List

from src.common.error_or import ErrorOr
from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.common.query import Query, QueryHandler
from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass(frozen=True)
class ListSubscriptions(Query):
    pass


class ListSubscriptionsHandler(QueryHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, query: ListSubscriptions) -> ErrorOr[List[Subscription]]:
        subscriptions = await self._subscriptions_repository.get_multi()
        return ErrorOr.from_result(subscriptions)
