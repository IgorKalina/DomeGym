import uuid

from src.gym_management.application.common.dto.repository import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


class GetSubscription(Query):
    subscription_id: uuid.UUID


class GetSubscriptionHandler(QueryHandler):
    def __init__(self, subscription_repository: SubscriptionRepository) -> None:
        self.__subscription_repository = subscription_repository

    async def handle(self, query: GetSubscription) -> SubscriptionDB:
        subscription_db: SubscriptionDB | None = await self.__subscription_repository.get_by_id(query.subscription_id)
        if subscription_db is None:
            raise SubscriptionDoesNotExistError()
        return subscription_db
