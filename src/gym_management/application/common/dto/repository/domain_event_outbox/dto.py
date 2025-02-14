import uuid
from typing import Self

from pydantic import Field

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.shared_kernel.application.dto import RepositoryDto
from src.shared_kernel.domain.common.event import DomainEvent


class DomainEventDB(RepositoryDto):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    event: DomainEvent
    processing_status: DomainEventProcessingStatus = DomainEventProcessingStatus.PENDING
    failure_reason: str | None = None

    def set_to_published(self) -> Self:
        self.processing_status = DomainEventProcessingStatus.PUBLISHED
        return self

    def set_to_failed(self) -> Self:
        self.processing_status = DomainEventProcessingStatus.FAILED
        return self

    def set_to_processed(self) -> Self:
        self.processing_status = DomainEventProcessingStatus.PROCESSED
        return self
