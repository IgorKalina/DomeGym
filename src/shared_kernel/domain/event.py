import abc
from abc import ABC
from typing import Generic, TypeVar

__all__ = ["DomainEvent", "DomainEventHandler", "EventType"]


class DomainEvent(ABC):
    pass


EventType = TypeVar("EventType", bound=DomainEvent)


class DomainEventHandler(ABC, Generic[EventType]):
    @abc.abstractmethod
    async def handle(self, event: EventType) -> None:
        pass
