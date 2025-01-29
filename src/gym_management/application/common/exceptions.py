import uuid
from dataclasses import dataclass

from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.domain.common.exceptions import DomainError


@dataclass(kw_only=True, frozen=True)
class AppError(DomainError):
    @property
    def detail(self) -> str:
        return "Unknown application error has occurred"


@dataclass(kw_only=True, frozen=True)
class DomainEventError(AppError):
    entity_name = "DomainEvent"
    error_type = ErrorType.UNEXPECTED

    @property
    def detail(self) -> str:
        return "Unknown domain event error has occurred"


@dataclass(kw_only=True, frozen=True)
class DomainEventDoesNotExistError(DomainEventError):
    event_id: uuid.UUID
    error_type = ErrorType.UNEXPECTED

    @property
    def detail(self) -> str:
        return f"Domain event with the provided id not found: {self.event_id}"
