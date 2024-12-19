from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

from src.common.error_or.errors.base import Error
from src.common.error_or.exceptions import InvalidOperationError

TValue = TypeVar("TValue", bound=Any)


@dataclass
class ErrorOr(Generic[TValue]):
    _value: Optional[TValue] = None
    _errors: List[Error] = field(default_factory=list)

    @property
    def value(self) -> Optional[TValue]:
        if self.is_error():
            raise InvalidOperationError(
                "The 'value' property cannot be accessed when errors have been recorded. "
                "Check 'is_error()' before accessing value."
            )
        return self._value

    @property
    def errors(self) -> List[Error]:
        if not self.is_error():
            raise InvalidOperationError(
                "The 'errors' property cannot be accessed when no errors have been recorded. "
                "Check 'is_error()'  before accessing errors."
            )
        return self._errors.copy()

    @property
    def first_error(self) -> Error:
        if not self.is_error():
            raise InvalidOperationError(
                "The 'first_error' property cannot be accessed when no errors have been recorded. "
                "Check 'is_error()' before accessing errors."
            )
        return self._errors[0]

    def is_error(self) -> bool:
        return bool(self._errors)

    def is_ok(self) -> bool:
        return not self.is_error()
