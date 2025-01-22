import logging
import typing
from typing import List

from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.application.event.domain.repository import FailedDomainEventRepository

if typing.TYPE_CHECKING:
    from src.shared_kernel.domain.event import DomainEvent

logger: logging.Logger = logging.getLogger(__name__)


async def reprocess_failed_domain_events(
    failed_events_repository: FailedDomainEventRepository, domain_eventbus: DomainEventBus
) -> None:
    failed_domain_events: List[DomainEvent] = await failed_events_repository.get_multi()
    if failed_domain_events:
        logger.info(f"Re-processing '{len(failed_domain_events)}' domain events")
        await domain_eventbus.publish(failed_domain_events)
        await domain_eventbus.process_events()
        await failed_events_repository.truncate()
    else:
        logger.info("No failed domain events to re-process")
