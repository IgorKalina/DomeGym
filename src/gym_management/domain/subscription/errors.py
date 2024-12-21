from dataclasses import dataclass

from src.shared_kernel.application.error_or import errors


@dataclass(frozen=True)
class SubscriptionCannotHaveMoreGymsThanSubscriptionAllows(errors.ValidationError):
    description: str = "A subscription cannot have more gyms than the subscription allows"

    @property
    def entity_name(self) -> str:
        return "Subscription"
