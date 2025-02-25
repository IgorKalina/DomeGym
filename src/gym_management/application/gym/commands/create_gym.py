import logging
import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.command import Command, CommandHandler

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription

logger = logging.getLogger(__name__)


class CreateGym(Command):
    name: str
    subscription_id: uuid.UUID


class CreateGymHandler(CommandHandler):
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        domain_event_repository: DomainEventRepository,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__domain_event_repository = domain_event_repository

    async def handle(self, command: CreateGym) -> Gym:
        subscription: Subscription = await self.__subscription_repository.get(command.subscription_id)
        gym = Gym(
            name=command.name,
            max_rooms=subscription.max_rooms,
            subscription_id=command.subscription_id,
        )
        subscription.add_gym(gym)

        await self.__subscription_repository.update(subscription)
        await self.__domain_event_repository.bulk_create(subscription.pop_domain_events())
        return gym
