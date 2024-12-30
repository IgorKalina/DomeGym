from dataclasses import dataclass

from src.gym_management.domain.common.exceptions import DomainError
from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True)
class GymDomainError(DomainError):
    entity_name: str = "Gym"

    @property
    def detail(self) -> str:
        return "Unknown Gym error has occurred"


@dataclass(kw_only=True)
class GymCannotHaveMoreRoomsThanSubscriptionAllowsError(GymDomainError):
    max_rooms: int
    error_type: ErrorType = ErrorType.VALIDATION

    @property
    def detail(self) -> str:
        return f"A gym cannot have more rooms than the subscription allows. Max rooms allowed: {self.max_rooms}"
