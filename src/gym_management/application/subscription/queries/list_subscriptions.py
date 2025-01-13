from dataclasses import dataclass
from typing import List

from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


@dataclass(frozen=True)
class ListSubscriptions(Query):
    pass


class ListSubscriptionsHandler(QueryHandler):
    def __init__(self, subscription_repository: SubscriptionRepository) -> None:
        self.__subscription_repository = subscription_repository

    async def handle(self, query: ListSubscriptions) -> List[SubscriptionDB]:  # noqa: ARG002
        return await self.__subscription_repository.get_multi()
