import uuid

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


class GetSubscription(Query):
    subscription_id: uuid.UUID


class GetSubscriptionHandler(QueryHandler):
    def __init__(self, subscription_repository: SubscriptionRepository) -> None:
        self.__subscription_repository = subscription_repository

    async def handle(self, query: GetSubscription) -> Subscription:
        return await self.__subscription_repository.get(query.subscription_id)
