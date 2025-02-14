import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class GetGym(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class GetGymHandler(QueryHandler):
    def __init__(self, gym_repository: GymRepository, subscription_repository: SubscriptionRepository) -> None:
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository

    async def handle(self, query: GetGym) -> Gym:
        subscription: Subscription = await self.__subscription_repository.get(query.subscription_id)
        if not subscription.has_gym(query.gym_id):
            raise GymDoesNotExistError()
        return await self.__gym_repository.get(query.gym_id)
