import logging

from src.gym_management.domain.subscription.events.gym_added_event import SomeEvent
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class SomeEventHandler(DomainEventHandler):
    async def handle(self, event: SomeEvent) -> None:
        logger.info(f"Handling '{event.__class__.__name__}' event")
        logger.info("Doing some loooooooong computation for some event")
        logger.info("Processing done!")
