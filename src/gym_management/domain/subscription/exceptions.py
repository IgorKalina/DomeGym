from dataclasses import dataclass

from src.gym_management.domain.common.exceptions import DomainError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True, frozen=True)
class SubscriptionDomainError(DomainError):
    entity_name: str = "Subscription"

    @property
    def detail(self) -> str:
        return "Unknown Subscription error has occurred"


@dataclass(kw_only=True, frozen=True)
class SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError(SubscriptionDomainError):
    max_gyms: int
    error_type: ErrorType = ErrorType.VALIDATION

    @property
    def detail(self) -> str:
        return f"A subscription cannot have more gyms than the subscription allows. Max gyms allowed: {self.max_gyms}"
