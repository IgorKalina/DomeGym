import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym

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
        subscription: Subscription | None = await self.__subscription_repository.get_or_none(event.subscription.id)
        if subscription is None:
            logger.warning("Subscription has been already unset")
            return
        await self.__remove_all_gyms(subscription)
        await self.__subscription_repository.delete(subscription)

    async def __remove_all_gyms(self, subscription: Subscription) -> None:
        logger.info(f"Removing all gyms for the removed subscription with id: {subscription.id}")
        gyms: List[Gym] = await self.__gym_repository.get_by_subscription_id(subscription.id)
        for gym in gyms:
            subscription.remove_gym(gym)
            logger.info(f"Removed gym with id '{gym.id}' from subscription id: {subscription.id}")

        await self.__domain_event_bus.publish(subscription.pop_domain_events())
        logger.info(f"All gyms have been removed for the subscription id: {subscription.id}")
