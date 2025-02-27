import asyncio
import logging
from typing import List

from dependency_injector.wiring import Provide, inject

from src.gym_management.application.common.dto.repository import DomainEventDB
from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.application.exceptions import EventualConsistencyError
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


@inject
async def process_domain_events(
    unit_of_work: UnitOfWork = Provide[DiContainer.repository_container.unit_of_work],
    domain_event_bus: DomainEventBus = Provide[DiContainer.domain_event_container.domain_event_bus],
    domain_event_repository: DomainEventRepository = (
        Provide[DiContainer.repository_container.domain_event_repository]
    ),
) -> None:
    async def handle_domain_event(dto: DomainEventDB) -> None:
        async with unit_of_work:
            try:
                await domain_event_bus.publish(dto.event)
                dto.set_to_processed()
            except EventualConsistencyError as e:
                dto.set_to_failed()
                dto.error = e.detail
            finally:
                await domain_event_repository.update(dto)

    while True:
        domain_events: List[DomainEventDB] = await domain_event_repository.list(
            status=DomainEventProcessingStatus.PENDING
        )
        if not domain_events:
            logger.info("No domain events to process")
            return

        logger.info(f"Processing {len(domain_events)} domain events")
        await asyncio.gather(*(handle_domain_event(dto) for dto in domain_events))
        logger.info("Batch processing complete.")
