from dataclasses import dataclass

from src.gym_management.application.common.exceptions import AppError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True, frozen=True)
class AdminAppError(AppError):
    entity_name: str = "Admin"

    @property
    def detail(self) -> str:
        return "Unknown Admin error has occurred"


@dataclass(kw_only=True, frozen=True)
class AdminAlreadyExistsError(AdminAppError):
    error_type: ErrorType = ErrorType.CONFLICT

    @property
    def detail(self) -> str:
        return "Admin with the provided id already exists"


@dataclass(kw_only=True, frozen=True)
class AdminDoesNotExistError(AdminAppError):
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return "Admin with the provided id does not exist"
