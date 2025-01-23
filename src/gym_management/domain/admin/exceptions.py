from dataclasses import dataclass

from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.domain.exceptions import DomainError


@dataclass(kw_only=True, frozen=True)
class AdminDomainError(DomainError):
    entity_name: str = "Admin"

    @property
    def detail(self) -> str:
        return "Unknown Admin error has occurred"


@dataclass(kw_only=True, frozen=True)
class AdminDoesNotHaveSubscriptionSetError(AdminDomainError):
    error_type: ErrorType = ErrorType.UNEXPECTED

    @property
    def detail(self) -> str:
        return "Admin with the provided id does not have a subscription set"
