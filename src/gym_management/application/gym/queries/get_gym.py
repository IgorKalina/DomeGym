import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.subscription.queries.get_subscription import GetSubscription
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository import SubscriptionDB


class GetGym(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class GetGymHandler(QueryHandler):
    def __init__(self, query_invoker: QueryInvoker, gym_repository: GymRepository) -> None:
        self.__gym_repository = gym_repository

        self.__query_invoker = query_invoker

    async def handle(self, query: GetGym) -> GymDB:
        subscription: Subscription = await self.__get_subscription(query)
        gym: GymDB | None = await self.__gym_repository.get_by_id(gym_id=query.gym_id, subscription_id=subscription.id)
        if gym is None:
            raise GymDoesNotExistError()
        return gym

    async def __get_subscription(self, query: GetGym) -> Subscription:
        get_subscription_query = GetSubscription(subscription_id=query.subscription_id)
        subscription_db: SubscriptionDB = await self.__query_invoker.invoke(get_subscription_query)
        return dto.mappers.subscription.db_to_domain(subscription_db)
