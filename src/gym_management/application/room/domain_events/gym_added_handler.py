import logging

from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.shared_kernel.domain.event import DomainEventHandler

logger = logging.getLogger(__name__)


class GymAddedEventHandler(DomainEventHandler):
    async def handle(self, event: GymAddedEvent) -> None:
        logger.info(f"Handling '{event.__class__.__name__}' event")
        logger.info(f"Doing some computation for room after {event.__class__.__name__} event...")
        logger.info("Processing done!")