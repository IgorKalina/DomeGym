import uuid
from abc import ABC, abstractmethod
from typing import List

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.dto.repository.domain_event_outbox.dto import DomainEventDB
from src.shared_kernel.domain.common.event import DomainEvent


# todo: split this into separate interfaces to follows ISP
class DomainEventRepository(ABC):
    @abstractmethod
    async def bulk_create(self, events: List[DomainEvent]) -> None:
        pass

    @abstractmethod
    async def get(self, event_id: uuid.UUID) -> DomainEventDB:
        pass

    @abstractmethod
    async def list(self, status: DomainEventProcessingStatus) -> List[DomainEventDB]:
        pass

    @abstractmethod
    async def update(self, event: DomainEventDB) -> DomainEventDB:
        pass

    @abstractmethod
    async def bulk_delete(self, event_ids: List[uuid.UUID]) -> None:
        pass
