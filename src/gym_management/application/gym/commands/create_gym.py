import logging
import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB

logger = logging.getLogger(__name__)


class CreateGym(Command):
    name: str
    subscription_id: uuid.UUID


class CreateGymHandler(CommandHandler):
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        gym_repository: GymRepository,
        eventbus: DomainEventBus,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__gym_repository = gym_repository
        self.__eventbus = eventbus

    async def handle(self, command: CreateGym) -> GymDB:
        subscription: Subscription = await self.__get_subscription_domain(command)
        gym = Gym(
            name=command.name,
            max_rooms=subscription.max_rooms,
            subscription_id=command.subscription_id,
        )
        subscription.add_gym(gym)

        gym_db: GymDB = await self.__create_gym_in_db(gym)
        await self.__create_domain_events_in_db(subscription)
        return gym_db

    async def __get_subscription_domain(self, command: CreateGym) -> Subscription:
        subscription_db: SubscriptionDB | None = await self.__subscription_repository.get_by_id(command.subscription_id)
        if subscription_db is None:
            raise SubscriptionDoesNotExistError()
        return dto.mappers.subscription.db_to_domain(subscription_db)

    async def __create_gym_in_db(self, gym: Gym) -> GymDB:
        gym_db: GymDB = dto.mappers.gym.domain_to_db(gym)
        await self.__gym_repository.create(gym_db)
        return gym_db

    async def __create_domain_events_in_db(self, subscription: Subscription) -> None:
        await self.__eventbus.publish(subscription.pop_domain_events())
