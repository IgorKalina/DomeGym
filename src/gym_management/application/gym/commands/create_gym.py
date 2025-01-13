import logging
import uuid
from dataclasses import dataclass

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.gym.dto.repository import GymDB
from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
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

        subscription = Subscription(
            id=subscription_db.id,
            type=subscription_db.type,
            admin_id=subscription_db.admin_id,
            gym_ids=subscription_db.gym_ids,
        )
        gym = Gym(name=command.name, max_rooms=subscription.max_rooms, subscription_id=command.subscription_id)
        subscription.add_gym(gym)

        subscription_db = SubscriptionDB(
            id=subscription.id,
            type=subscription.type,
            admin_id=subscription.admin_id,
            gym_ids=subscription.gym_ids,
        )
        gym_db = GymDB(id=gym.id, name=gym.name, subscription_id=gym.subscription_id)
        await self.__subscription_repository.update(subscription_db)
        await self.__gym_repository.create(gym_db)
        await self.__eventbus.publish(subscription.pop_domain_events())
        return gym_db
