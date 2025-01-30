import logging

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventOutboxRepository,
)

logger = logging.getLogger(__name__)


async def publish_domain_events(
    domain_event_outbox_repository: DomainEventOutboxRepository,
) -> None:
    logger.info("Publishing domain events...")
    domain_events = await domain_event_outbox_repository.get_multi(status=DomainEventProcessingStatus.PENDING)
    for event in domain_events:
        logger.info(f"Sending domain event to the domain events topic: {event}")
        logger.info(f"Updating its status to PUBLISHED: {event}")
