from dataclasses import dataclass

from src.shared_kernel.application.error_or import errors


@dataclass(frozen=True)
class RoomDoesNotExist(errors.NotFoundError):
    description: str = "Room does not exist in the gym"

    @property
    def entity_name(self) -> str:
        return "Room"
