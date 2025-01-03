import abc
from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

__all__ = ["DomainEvent", "DomainEventHandler", "EventType"]


@dataclass(kw_only=True)
class DomainEvent(ABC):
    pass


EventType = TypeVar("EventType", bound=DomainEvent)


class DomainEventHandler(ABC, Generic[EventType]):
    @abc.abstractmethod
    async def handle(self, event: EventType) -> None:
        pass
