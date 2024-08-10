from dataclasses import dataclass
from typing import Any

from .error_type import ErrorType


@dataclass(frozen=True)
class Error:
    type: ErrorType
    description: str

    @property
    def entity_name(self) -> str:
        return "General"

    @property
    def code(self) -> str:
        return f"{self.entity_name.capitalize()}.{self.type.name.capitalize()}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self.code == other.code and self.description == other.description and self.type == other.type:
            return True
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.code, self.description, self.type))
