import uuid
from dataclasses import dataclass

from src.gym_management.application.common.exceptions import AppError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True, frozen=True)
class RoomAppError(AppError):
    entity_name: str = "Room"

    @property
    def detail(self) -> str:
        return "Unknown Room error has occurred"


@dataclass(kw_only=True, frozen=True)
class RoomDoesNotExistError(RoomAppError):
    room_id: uuid.UUID
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return f"Room with the provided id does not exist: {self.room_id}"
