from dataclasses import dataclass

from src.shared_kernel.application.error_or import errors


@dataclass(frozen=True)
class GymCannotHaveMoreRoomsThanSubscriptionAllows(errors.ValidationError):
    description: str = "A gym cannot have more rooms than the subscription allows"

    @property
    def entity_name(self) -> str:
        return "Gym"
