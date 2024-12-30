import typing
import uuid
from dataclasses import dataclass

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass(kw_only=True, frozen=True)
class GetGym(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class GetGymHandler(QueryHandler):
    def __init__(self, subscription_repository: SubscriptionRepository, gym_repository: GymRepository) -> None:
        self.__subscription_repository = subscription_repository
        self.__gym_repository = gym_repository

    async def handle(self, query: GetGym) -> Gym:
        subscription: Subscription | None = await self.__subscription_repository.get_by_id(query.subscription_id)
        if subscription is None:
            raise SubscriptionDoesNotExistError()

        gym: Gym | None = await self.__gym_repository.get_by_id(query.gym_id)
        if gym is None:
            raise GymDoesNotExistError()
        return gym
