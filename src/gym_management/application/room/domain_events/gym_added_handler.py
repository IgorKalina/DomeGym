import logging

from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class GymAddedEventHandler(DomainEventHandler):
    def __init__(self, domain_event_bus: DomainEventBus) -> None:
        self.__domain_event_bus = domain_event_bus

    async def handle(self, event: GymAddedEvent) -> None:
        logger.info(f"Handling '{event.__class__.__name__}' event")
        logger.info(f"Doing some computation for room after {event.__class__.__name__} event...")
        logger.info("Processing done!")
        await self.__domain_event_bus.publish([SomeEvent()])
