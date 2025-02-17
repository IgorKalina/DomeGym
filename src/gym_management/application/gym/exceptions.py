import uuid
from dataclasses import dataclass

from src.gym_management.application.common.exceptions import AppError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True, frozen=True)
class GymAppError(AppError):
    entity_name: str = "Gym"

    @property
    def detail(self) -> str:
        return "Unknown Gym error has occurred"


@dataclass(kw_only=True, frozen=True)
class GymDoesNotExistError(GymAppError):
    gym_id: uuid.UUID
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return f"Gym with the provided id not found: {self.gym_id}"


@dataclass(kw_only=True, frozen=True)
class GymAlreadyExistsError(GymAppError):
    gym_id: uuid.UUID
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return f"Gym with the provided id already exists: {self.gym_id}"
