from dataclasses import dataclass

from .base import Error
from .error_type import ErrorType


@dataclass(frozen=True)
class FailureError(Error):
    type: ErrorType = ErrorType.FAILURE
    description: str = "A failure has occurred."


@dataclass(frozen=True)
class UnexpectedError(Error):
    type: ErrorType = ErrorType.UNEXPECTED
    description: str = "An unexpected error has occurred."


@dataclass(frozen=True)
class ValidationError(Error):
    type: ErrorType = ErrorType.VALIDATION
    description: str = "A validation error has occurred."


@dataclass(frozen=True)
class ConflictError(Error):
    type: ErrorType = ErrorType.CONFLICT
    description: str = "A conflict error has occurred."


@dataclass(frozen=True)
class NotFoundError(Error):
    type: ErrorType = ErrorType.NOT_FOUND
    description: str = "A 'Not Found' error has occurred."


@dataclass(frozen=True)
class UnauthorizedError(Error):
    type: ErrorType = ErrorType.UNAUTHORIZED
    description: str = "An 'Unauthorized' error has occurred."


@dataclass(frozen=True)
class ForbiddenError(Error):
    type: ErrorType = ErrorType.FORBIDDEN
    description: str = "A 'Forbidden' error has occurred."
