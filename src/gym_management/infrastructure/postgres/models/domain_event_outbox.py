import uuid
from typing import List, Self, Type

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.application.common.dto.repository import DomainEventDB
from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.infrastructure.postgres.models.base_model import TimedBaseModel
from src.shared_kernel.domain.common.event import DomainEvent


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
        return cls(
            id=dto.event.id,
            event_type=type(dto.event).__name__,
            event_data=dto.event.model_dump(),
            processing_status=dto.processing_status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_dto(self) -> DomainEventDB:
        domain_event_class = self.__map_event_type_to_event_class()
        return DomainEventDB(
            id=self.id,
            event=domain_event_class(**self.event_data),
            processing_status=self.processing_status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __map_event_type_to_event_class(self) -> Type[DomainEvent]:
        subclasses: List[Type[DomainEvent]] = DomainEvent.__subclasses__()
        for subclass in subclasses:
            if subclass.__name__ == self.event_type:
                return subclass
        raise TypeError(f"Domain event type '{self.event_type}' does not exist")
