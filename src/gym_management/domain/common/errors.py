from dataclasses import dataclass
from enum import Enum, auto

from result import Err

__all__ = [
    "FailureError",
    "UnexpectedError",
    "ValidationError",
    "ConflictError",
    "NotFoundError",
    "UnauthorizedError",
    "ForbiddenError",
]


class ErrorType(Enum):
    FAILURE = auto()
    UNEXPECTED = auto()
    VALIDATION = auto()
    CONFLICT = auto()
    NOT_FOUND = auto()
    UNAUTHORIZED = auto()
    FORBIDDEN = auto()


@dataclass
class ErrorDetails:
    title: str
    description: str


class Error(Err):
    _type: ErrorType

    def __init__(self, title: str, description: str) -> None:
        error = ErrorDetails(title=title, description=description)
        super().__init__(error)

    def err(self) -> ErrorDetails:
        return self._value

    def get_error_type(self) -> ErrorType:
        return self._type


class FailureError(Error):
    _type = ErrorType.FAILURE


class UnexpectedError(Error):
    _type = ErrorType.UNEXPECTED


class ValidationError(Error):
    _type = ErrorType.VALIDATION


class ConflictError(Error):
    _type = ErrorType.CONFLICT


class NotFoundError(Error):
    _type = ErrorType.NOT_FOUND


class UnauthorizedError(Error):
    _type = ErrorType.UNAUTHORIZED


class ForbiddenError(Error):
    _type = ErrorType.FORBIDDEN
