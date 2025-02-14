import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription

    pass


class GetGym(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class GetGymHandler(QueryHandler):
    def __init__(
        self, gym_repository: GymRepository, subscription_repository: SubscriptionRepository, query_bus: QueryBus
    ) -> None:
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository

        self.__query_bus = query_bus

    async def handle(self, query: GetGym) -> GymDB:
        subscription: Subscription = await self.__subscription_repository.get(query.subscription_id)
        gym: GymDB | None = await self.__gym_repository.get_by_id(gym_id=query.gym_id, subscription_id=subscription.id)
        if gym is None:
            raise GymDoesNotExistError()
        return gym
