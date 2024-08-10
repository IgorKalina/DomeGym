from dataclasses import dataclass
from typing import Iterable, Sequence

from . import errors
from .error_or import ErrorOr, TValue
from .errors import (
    ConflictError,
    Error,
    ErrorType,
    FailureError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    UnexpectedError,
    ValidationError,
)
from .results import Result, ResultType

__all__ = [
    "ErrorOr",
    "OkResult",
    "ErrorResult",
    "Error",
    "ErrorType",
    "errors",
    "Result",
    "ResultType",
]


@dataclass
class OkResult(ErrorOr[TValue]):
    def __init__(self, value: TValue) -> None:
        super().__init__(_value=value)


@dataclass
class ErrorResult(ErrorOr[TValue]):
    def __init__(self, error: Error | Sequence[Error]) -> None:
        if isinstance(error, Iterable):
            error_list = list(error)
        else:
            error_list = [error]
        super().__init__(_errors=error_list)
