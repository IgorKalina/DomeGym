import logging
import uuid
from typing import TYPE_CHECKING, List

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
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
        subscription_db: SubscriptionDB | None = await self.__subscription_repository.get_by_id(command.subscription_id)
        if subscription_db is None:
            raise SubscriptionDoesNotExistError()
        gyms: List[GymDB] = await self.__gym_repository.get_by_subscription_id(subscription_db.id)

        subscription = dto.mappers.subscription.db_to_domain(subscription=subscription_db, gyms=gyms)
        gym = Gym(
            name=command.name,
            max_rooms=subscription.max_rooms,
            subscription_id=command.subscription_id,
        )
        subscription.add_gym(gym)

        subscription_db = dto.mappers.subscription.domain_to_db(subscription)
        gym_db: GymDB = dto.mappers.gym.domain_to_db(gym=gym)
        await self.__subscription_repository.update(subscription_db)
        await self.__gym_repository.create(gym_db)
        await self.__eventbus.publish(subscription.pop_domain_events())
        return gym_db
