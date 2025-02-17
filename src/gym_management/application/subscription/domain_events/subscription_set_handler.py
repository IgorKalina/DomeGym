import logging

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class SubscriptionSetHandler(DomainEventHandler):
    """
    Remove all gyms per subscription
    """

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__domain_event_bus = domain_event_bus

    async def handle(self, event: SubscriptionUnsetEvent) -> None:
        await self.__subscription_repository.create(event.subscription)
        logger.info(f"Created a new subscription: {event.subscription}")
