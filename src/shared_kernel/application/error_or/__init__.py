from dataclasses import dataclass
from typing import Iterable, Sequence

from . import errors
from .error_or import ErrorOr, ValueType
from .errors import Error, ErrorType
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
class OkResult(ErrorOr[ValueType]):
    def __init__(self, value: ValueType) -> None:
        super().__init__(_value=value)


@dataclass
class ErrorResult(ErrorOr[ValueType]):
    def __init__(self, error: Error | Sequence[Error]) -> None:
        super().__init__(_errors=list(error) if isinstance(error, Iterable) else [error])
