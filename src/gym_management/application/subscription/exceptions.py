from dataclasses import dataclass

from src.gym_management.application.common.exceptions import AppError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True)
class SubscriptionAppError(AppError):
    entity_name: str = "Subscription"

    @property
    def detail(self) -> str:
        return "Unknown Subscription error has occurred"


@dataclass(kw_only=True)
class SubscriptionDoesNotExistError(SubscriptionAppError):
    error_type: ErrorType = ErrorType.NOT_FOUND

    @property
    def detail(self) -> str:
        return "Subscription with the provided id not found"
