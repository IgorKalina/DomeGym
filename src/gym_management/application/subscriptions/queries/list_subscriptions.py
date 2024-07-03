from dataclasses import dataclass

from result import Ok, Result

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.common.query import Query, QueryHandler


@dataclass(frozen=True)
class ListSubscriptions(Query):
    pass


class ListSubscriptionsHandler(QueryHandler):
    def __init__(self, subscriptions_repository: SubscriptionsRepository) -> None:
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, query: ListSubscriptions) -> Result:
        subscriptions = await self._subscriptions_repository.get_multi()
        return Ok(subscriptions)
