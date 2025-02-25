import uuid
from typing import List

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.application.common.dto.repository.domain_event_outbox.dto import DomainEventDB
from src.gym_management.application.common.exceptions import DomainEventDoesNotExistError
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.models.domain_event import DomainEventOutbox
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository
from src.shared_kernel.domain.common.event import DomainEvent


class DomainEventPostgresRepository(SQLAlchemyRepository, DomainEventRepository):
    async def bulk_create(self, events: List[DomainEvent]) -> None:
        domain_events_dto = [DomainEventDB(event=domain_event) for domain_event in events]
        domain_event_outboxes = [DomainEventOutbox.from_dto(dto) for dto in domain_events_dto]
        self._session.add_all(domain_event_outboxes)
        await self._session.flush(domain_event_outboxes)

    async def get(self, event_id: uuid.UUID) -> DomainEventDB:
        query = select(models.DomainEventOutbox).where(models.DomainEventOutbox.id == event_id)
        result = await self._session.scalars(query)
        domain_event: models.DomainEventOutbox | None = result.one_or_none()
        if domain_event is None:
            raise DomainEventDoesNotExistError(event_id=event_id)
        return domain_event.to_dto()

    async def list(self, status: DomainEventProcessingStatus) -> List[DomainEventDB]:
        try:
            result = await self._session.execute(
                select(DomainEventOutbox).filter(DomainEventOutbox.processing_status == status)
            )
            domain_event_outboxes = result.scalars().all()
            return [domain_event_outbox.to_dto() for domain_event_outbox in domain_event_outboxes]
        except NoResultFound:
            return []

    async def update(self, event: DomainEventDB) -> DomainEventDB:
        domain_event_db = await self._session.get(models.DomainEventOutbox, event.id)
        if not domain_event_db:
            raise DomainEventDoesNotExistError(event_id=event.event.id)

        domain_event_db_updated = models.DomainEventOutbox.from_dto(event)
        await self._session.merge(domain_event_db_updated)
        await self._session.flush((domain_event_db_updated,))
        return domain_event_db_updated.to_dto()

    async def bulk_delete(self, event_ids: List[uuid.UUID]) -> None:
        query = delete(DomainEventOutbox).where(DomainEventOutbox.id.in_(event_ids))
        await self._session.execute(query)
