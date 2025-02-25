import logging
from typing import TYPE_CHECKING

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.domain.subscription import Subscription

logger = logging.getLogger(__name__)


class SubscriptionSetHandler(DomainEventHandler):
    """
    Remove all gyms per subscription
    """

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self.__subscription_repository = subscription_repository

    async def handle(self, event: SubscriptionUnsetEvent) -> None:
        subscription: Subscription | None = await self.__subscription_repository.get_or_none(event.subscription.id)
        if subscription is None:
            await self.__subscription_repository.create(event.subscription)
            logger.info(f"Created a new subscription: {event.subscription}")
        else:
            logger.warning(
                f"Subscription with id '{event.subscription.id}' already exists. Skip subscription creation."
            )
