import logging
import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription

logger = logging.getLogger(__name__)


class RemoveGym(Command):
    subscription_id: uuid.UUID
    gym_id: uuid.UUID


class RemoveGymHandler(CommandHandler):
    def __init__(
        self,
        gym_repository: GymRepository,
        subscription_repository: SubscriptionRepository,
        query_bus: QueryBus,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository

        self.__domain_event_bus = domain_event_bus
        self.__query_bus = query_bus

    async def handle(self, command: RemoveGym) -> Gym:
        subscription: Subscription = await self.__subscription_repository.get(command.subscription_id)
        gym: Gym = await self.__gym_repository.get(command.gym_id)
        subscription.remove_gym(gym)

        await self.__gym_repository.delete(gym)
        await self.__domain_event_bus.publish(subscription.pop_domain_events())
        logger.info(f"Removed gym with id: {gym.id}")
        return gym
