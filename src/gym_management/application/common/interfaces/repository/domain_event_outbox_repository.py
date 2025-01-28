import uuid
from abc import ABC, abstractmethod
from typing import List

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.dto.repository.domain_event_outbox.dto import DomainEventDB


class DomainEventOutboxRepository(ABC):
    @abstractmethod
    async def create_multi(self, events: List[DomainEventDB]) -> None:
        pass

    @abstractmethod
    async def get_multi(self, status: DomainEventProcessingStatus) -> List[DomainEventDB]:
        pass

    @abstractmethod
    async def update(self, event: DomainEventDB) -> DomainEventDB:
        pass

    @abstractmethod
    async def delete_multi(self, event_ids: List[uuid.UUID]) -> DomainEventDB:
        pass
