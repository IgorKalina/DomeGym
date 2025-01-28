from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.shared_kernel.application.dto import RepositoryDto
from src.shared_kernel.domain.common.event import DomainEvent


class DomainEventDB(RepositoryDto):
    event: DomainEvent
    processing_status: DomainEventProcessingStatus = DomainEventProcessingStatus.PENDING
    failure_reason: str | None = None
