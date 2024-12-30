import logging
import uuid
from dataclasses import dataclass

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.eventbus import EventBus

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
        eventbus: EventBus,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__gym_repository = gym_repository
        self.__eventbus = eventbus

    async def handle(self, command: CreateGym) -> Gym:
        subscription = await self.__subscription_repository.get_by_id(command.subscription_id)
        if subscription is None:
            raise SubscriptionDoesNotExistError()

        gym = Gym(name=command.name, max_rooms=subscription.max_rooms, subscription_id=command.subscription_id)
        subscription.add_gym(gym)
        await self.__subscription_repository.update(subscription)
        await self.__gym_repository.create(gym)
        await self.__eventbus.publish(subscription.pop_domain_events())
        return gym
