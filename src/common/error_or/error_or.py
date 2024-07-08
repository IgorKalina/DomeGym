from dataclasses import dataclass, field
from typing import Any, Generic, Iterable, List, Optional, Sequence, TypeVar

from src.common.error_or.errors.base import Error
from src.common.error_or.exceptions import InvalidOperationException

TValue = TypeVar("TValue", bound=Any)


@dataclass
class ErrorOr(Generic[TValue]):
    _value: Optional[TValue] = None
    _errors: List[Error] = field(default_factory=list)

    @property
    def value(self) -> Optional[TValue]:
        if self.is_error():
            raise InvalidOperationException(
                "The 'value' property cannot be accessed when errors have been recorded. "
                "Check 'is_error()' before accessing value."
            )
        return self._value

    @property
    def errors(self) -> List[Error]:
        if not self.is_error():
            raise InvalidOperationException(
                "The 'errors' property cannot be accessed when no errors have been recorded. "
                "Check 'is_error()'  before accessing errors."
            )
        return self._errors.copy()

    @property
    def first_error(self) -> Error:
        if not self.is_error():
            raise InvalidOperationException(
                "The 'first_error' property cannot be accessed when no errors have been recorded. "
                "Check 'is_error()' before accessing errors."
            )
        return self._errors[0]

    def is_error(self) -> bool:
        return bool(self._errors)

    def is_ok(self) -> bool:
        return not self.is_error()

    @classmethod
    def from_result(cls, result: TValue) -> "ErrorOr":
        return cls(_value=result)

    @classmethod
    def from_error(cls, error: Error) -> "ErrorOr":
        return cls(_errors=[error])

    @classmethod
    def from_multi_errors(cls, errors: List[Error]) -> "ErrorOr":
        return cls(_errors=errors)


@dataclass
class OkResult(ErrorOr[TValue]):
    def __init__(self, value: TValue) -> None:
        super().__init__(_value=value)


@dataclass
class ErrorResult(ErrorOr[TValue]):
    def __init__(self, error: Error | Sequence[Error]) -> None:
        if isinstance(error, Iterable):
            errors = list(error)
        else:
            errors = [error]
        super().__init__(_errors=errors)
