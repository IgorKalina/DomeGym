from dataclasses import dataclass
from typing import Any, Optional

from .error_type import ErrorType


@dataclass(kw_only=True, frozen=True)
class Error:
    code: Optional[str] = ""
    description: Optional[str] = ""
    type: ErrorType

    @classmethod
    def failure(
        cls,
        code: Optional[str] = "General.Failure",
        description: Optional[str] = "A failure has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.FAILURE)

    @classmethod
    def unexpected(
        cls,
        code: Optional[str] = "General.Unexpected   ",
        description: Optional[str] = "An unexpected error has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.UNEXPECTED)

    @classmethod
    def validation(
        cls,
        code: Optional[str] = "General.Validation",
        description: Optional[str] = "A validation error has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.VALIDATION)

    @classmethod
    def conflict(
        cls,
        code: Optional[str] = "General.Conflict",
        description: Optional[str] = "A conflict error has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.CONFLICT)

    @classmethod
    def not_found(
        cls,
        code: Optional[str] = "General.NotFound",
        description: Optional[str] = "A 'Not Found' error has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.NOT_FOUND)

    @classmethod
    def unauthorized(
        cls,
        code: Optional[str] = "General.Unauthorized",
        description: Optional[str] = "An 'Unauthorized' error has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.UNAUTHORIZED)

    @classmethod
    def forbidden(
        cls,
        code: Optional[str] = "General.Forbidden",
        description: Optional[str] = "A 'Forbidden' error has occurred.",
    ) -> "Error":
        return cls(code=code, description=description, type=ErrorType.FORBIDDEN)

    @classmethod
    def custom(
        cls,
        code: str,
        description: str,
        # todo: think of a dynamic enum
        error_type: Any,
    ) -> "Error":
        return cls(code=code, description=description, type=error_type)

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
