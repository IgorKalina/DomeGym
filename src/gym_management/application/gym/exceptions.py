from dataclasses import dataclass

from src.gym_management.application.common.exceptions import AppError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True)
class GymAppError(AppError):
    entity_name: str = "Gym"

    @property
    def detail(self) -> str:
        return "Unknown Gym error has occurred"


@dataclass(kw_only=True)
class GymDoesNotExistError(GymAppError):
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return "Gym with the provided id not found"
