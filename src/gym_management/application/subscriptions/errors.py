from dataclasses import dataclass

from src.shared_kernel.error_or.errors import errors


@dataclass(frozen=True)
class AdminAlreadyExists(errors.ConflictError):
    description: str = "Admin with the provided id already exists"

    @property
    def entity_name(self) -> str:
        return "Admin"


@dataclass(frozen=True)
class SubscriptionDoesNotExist(errors.NotFoundError):
    description: str = "Subscription with the provided id not found"

    @property
    def entity_name(self) -> str:
        return "Subscription"
