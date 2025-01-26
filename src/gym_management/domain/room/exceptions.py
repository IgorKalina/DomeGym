from dataclasses import dataclass

from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.domain.common.exceptions import DomainError


@dataclass(kw_only=True, frozen=True)
class RoomError(DomainError):
    entity_name: str = "Room"

    @property
    def detail(self) -> str:
        return "Unknown Room error has occurred"


@dataclass(kw_only=True, frozen=True)
class RoomDoesNotExistError(RoomError):
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return "Room does not exist in the gym"
