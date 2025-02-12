import logging
from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.commands.remove_gym import RemoveGym
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.shared_kernel.application.command import CommandBus
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class SubscriptionUnsetHandler(DomainEventHandler):
    """
    Remove all gyms per subscription
    """

    def __init__(self, gym_repository: GymRepository, command_bus: CommandBus) -> None:
        self.__gym_repository = gym_repository

        self.__command_bus = command_bus

    async def handle(self, event: SubscriptionUnsetEvent) -> None:
        logger.info(f"Removing all gyms for the removed subscription with id: {event.subscription.id}")
        gyms: List[GymDB] = await self.__gym_repository.get_by_subscription_id(event.subscription.id)
        for gym_db in gyms:
            await self.__remove_gym(gym_db)
        logger.info(f"All gyms have been removed for the subscription id: {event.subscription.id}")

    async def __remove_gym(self, gym_db: GymDB) -> None:
        remove_gym_command = RemoveGym(
            subscription_id=gym_db.subscription_id,
            gym_id=gym_db.id,
        )
        await self.__command_bus.invoke(remove_gym_command)
