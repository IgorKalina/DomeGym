import logging
from typing import List

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.domain.admin.events.subscription_removed_event import SubscriptionRemovedEvent
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.domain.event import DomainEventHandler

logger = logging.getLogger(__name__)


class SubscriptionRemovedHandler(DomainEventHandler):
    """
    Remove all gyms per subscription
    """

    def __init__(self, gym_repository: GymRepository, eventbus: DomainEventBus) -> None:
        self.__gym_repository = gym_repository
        self.__eventbus = eventbus

    async def handle(self, event: SubscriptionRemovedEvent) -> None:
        logger.info(f"Removing all gyms for the removed subscription with id: {event.subscription.id}")
        gyms: List[GymDB] = await self.__gym_repository.get_by_subscription_id(event.subscription.id)
        for gym_db in gyms:
            await self.__remove_gym(gym_db=gym_db, event=event)
        logger.info(f"All gyms have been removed for the subscription id: {event.subscription.id}")

    async def __remove_gym(self, gym_db: GymDB, event: SubscriptionRemovedEvent) -> None:
        gym = dto.mappers.gym.db_to_domain(gym=gym_db, subscription=event.subscription)
        event.subscription.remove_gym(gym)
        await self.__gym_repository.delete(gym_db)
        await self.__eventbus.publish(event.subscription.pop_domain_events())
        logger.info(f"Removed gym with id: {gym_db.id}")
