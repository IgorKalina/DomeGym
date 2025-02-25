import logging
from typing import TYPE_CHECKING, List

from dependency_injector.wiring import Provide, inject

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.application.exceptions import EventualConsistencyError

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository import DomainEventDB

logger = logging.getLogger(__name__)


@inject
async def process_domain_events(
    di: DiContainer = Provide[DiContainer],
    # unit_of_work: UnitOfWork = Provide[DiContainer.repository_container.unit_of_work],
    # domain_event_bus: DomainEventBus = Provide[DiContainer.domain_event_container.domain_event_bus],
    # domain_event_repository: DomainEventRepository = (
    #     Provide[DiContainer.repository_container.domain_event_repository],
    # ),
) -> None:
    domain_event_repository = await di.repository_container.domain_event_repository()
    domain_event_bus = await di.domain_event_container.domain_event_bus()
    unit_of_work = await di.repository_container.unit_of_work()

    # todo: add ascending sorting
    domain_events: List[DomainEventDB] = await domain_event_repository.list(status=DomainEventProcessingStatus.PENDING)
    if not domain_events:
        logger.info("No domain events to process")
        return

    while domain_events:
        logger.info(f"Start processing {len(domain_events)} domain events")
        for dto in domain_events:
            async with unit_of_work:
                try:
                    await domain_event_bus.publish(dto.event)
                except EventualConsistencyError as e:
                    dto.set_to_failed()
                    dto.error = e.detail
                    await domain_event_repository.update(dto)
                else:
                    await domain_event_repository.update(dto.set_to_processed())

        logger.info(f"Processed {len(domain_events)} domain events")

        # Fetch the next batch of pending events
        domain_events = await domain_event_repository.list(status=DomainEventProcessingStatus.PENDING)
