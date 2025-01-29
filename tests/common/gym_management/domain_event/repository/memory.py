import uuid
from typing import List

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.dto.repository.domain_event_outbox.dto import DomainEventDB
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventOutboxRepository,
)


class DomainEventOutboxMemoryRepository(DomainEventOutboxRepository):
    def __init__(self) -> None:
        self.__domain_events: List[DomainEventDB] = []

    async def create_multi(self, events: List[DomainEventDB]) -> None:
        self.__domain_events.extend(events)

    async def get_multi(self, status: DomainEventProcessingStatus) -> List[DomainEventDB]:
        return [event for event in self.__domain_events if event.processing_status == status]

    async def update(self, event: DomainEventDB) -> DomainEventDB:
        updated_events = [e for e in self.__domain_events if e.id != event.id]
        updated_events.append(event)
        self.__domain_events = updated_events
        return event

    async def delete_multi(self, event_ids: List[uuid.UUID]) -> None:
        self.__domain_events = [event for event in self.__domain_events if event.id not in event_ids]
