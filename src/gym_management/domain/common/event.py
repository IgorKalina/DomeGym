import abc
from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

__all__ = [
    "DomainEvent",
    "DomainEventHandler",
]


@dataclass(kw_only=True)
class DomainEvent(ABC):
    pass


ET = TypeVar("ET", bound=DomainEvent)
ER = TypeVar("ER", bound=Any)


@dataclass
class DomainEventHandler(ABC, Generic[ET, ER]):
    @abc.abstractmethod
    def handle(self, event: ET) -> ER:
        pass
