import logging

from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class GymAddedEventHandler(DomainEventHandler):
    def __init__(self, eventbus: DomainEventBus) -> None:
        self.__eventbus = eventbus

    async def handle(self, event: GymAddedEvent) -> None:
        logger.info(f"Handling '{event.__class__.__name__}' event")
        logger.info(f"Doing some computation for room after {event.__class__.__name__} event...")
        logger.info("Processing done!")
        await self.__eventbus.publish([SomeEvent()])
