import logging

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventOutboxRepository,
)
from src.gym_management.infrastructure.common.background_services.domain_events.publisher import DomainEventPublisher

logger = logging.getLogger(__name__)


async def publish_domain_events(
    domain_event_outbox_repository: DomainEventOutboxRepository, event_publisher: DomainEventPublisher
) -> None:
    domain_events = await domain_event_outbox_repository.get_multi(status=DomainEventProcessingStatus.PENDING)
    logger.info(f"Publishing '{len(domain_events)}' domain events")
    for event in domain_events:
        await event_publisher.publish(event)
        await domain_event_outbox_repository.update(event.set_to_published())
        logger.debug(f"event id was published and the status was set to PUBLISHED: {event.id}")
