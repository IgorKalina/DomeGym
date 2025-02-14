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
    DomainEventOutboxRepository,
)
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.models.domain_event_outbox import DomainEventOutbox
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class DomainEventOutboxPostgresRepository(SQLAlchemyRepository, DomainEventOutboxRepository):
    async def create_multi(self, events: List[DomainEventDB]) -> None:
        domain_event_outboxes = [DomainEventOutbox.from_dto(event) for event in events]
        self._session.add_all(domain_event_outboxes)
        await self._session.commit()

    async def get_multi(self, status: DomainEventProcessingStatus) -> List[DomainEventDB]:
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
        await self._session.commit()
        return domain_event_db_updated.to_dto()

    async def delete_multi(self, event_ids: List[uuid.UUID]) -> None:
        query = delete(DomainEventOutbox).where(DomainEventOutbox.id.in_(event_ids))
        await self._session.execute(query)
        await self._session.commit()
