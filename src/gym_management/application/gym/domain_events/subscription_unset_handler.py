import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common import dto
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.subscription.aggregate_root import Subscription

logger = logging.getLogger(__name__)


class SubscriptionUnsetHandler(DomainEventHandler):
    """
    Remove all gyms per subscription
    """

    def __init__(
        self,
        gym_repository: GymRepository,
        subscription_repository: SubscriptionRepository,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository
        self.__domain_event_bus = domain_event_bus

    async def handle(self, event: SubscriptionUnsetEvent) -> None:
        logger.info(f"Removing all gyms for the removed subscription with id: {event.subscription.id}")
        await self.__remove_all_gyms_for_subscription(event)
        logger.info(f"All gyms have been removed for the subscription id: {event.subscription.id}")

    async def __remove_all_gyms_for_subscription(self, event: SubscriptionUnsetEvent) -> None:
        gyms: List[Gym] = await self.__gym_repository.get_by_subscription_id(event.subscription.id)
        subscription: Subscription = dto.mappers.subscription.subscription_unset_event_to_domain(event, gyms=gyms)
        for gym in gyms:
            subscription.remove_gym(gym)
            await self.__gym_repository.delete(gym)
            logger.info(f"Removed gym with id: {gym.id}")

        await self.__domain_event_bus.publish(subscription.pop_domain_events())
