from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

__all__ = [
    "ValueObject",
]


VT = TypeVar("VT", bound=Any)


@dataclass(frozen=True)
class ValueObject(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self._validate()

    @abstractmethod
    def to_raw(self) -> VT:
        pass

    @abstractmethod
    def _validate(self):
        pass
