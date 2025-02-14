import uuid
from typing import Self

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.application.common.dto.repository import DomainEventDB
from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.infrastructure.common.background_services.domain_events.event_registry.registry import (
    DomainEventRegistry,
)
from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class DomainEventOutbox(TimedBaseModel):
    __tablename__ = "domain_event_outbox"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(200))
    event_data: Mapped[dict] = mapped_column(JSONB)
    processing_status: Mapped[DomainEventProcessingStatus] = mapped_column(Enum(DomainEventProcessingStatus))

    def __repr__(self) -> str:
        return f"DomainEventOutbox(id={self.id!r}, name={self.event_type!r}"

    @classmethod
    def from_dto(cls, dto: DomainEventDB) -> Self:
        registry = DomainEventRegistry()
        return cls(
            id=dto.event.id,
            event_type=registry.get_event_type(dto.event),
            event_data=dto.event.model_dump(),
            processing_status=dto.processing_status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_dto(self) -> DomainEventDB:
        registry = DomainEventRegistry()
        return DomainEventDB(
            id=self.id,
            event=registry.get_event_type(self.event_type),
            processing_status=self.processing_status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
