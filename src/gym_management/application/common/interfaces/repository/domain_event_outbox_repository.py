import uuid
from abc import ABC, abstractmethod
from typing import List

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.dto.repository.domain_event_outbox.dto import DomainEventDB


class DomainEventOutboxRepository(ABC):
    @abstractmethod
    def create(self, event: DomainEventDB) -> None:
        pass

    @abstractmethod
    def get_multi(self, status: DomainEventProcessingStatus) -> List[DomainEventDB]:
        pass

    @abstractmethod
    def update(self, event: DomainEventDB) -> DomainEventDB:
        pass

    @abstractmethod
    def delete_multi(self, event_ids: List[uuid.UUID]) -> DomainEventDB:
        pass
