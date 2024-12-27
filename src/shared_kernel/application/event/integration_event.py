import abc
from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

__all__ = ["IntegrationEvent", "IntegrationEventHandler", "EventType"]


class IntegrationEvent(ABC):
    pass


EventType = TypeVar("EventType", bound=IntegrationEvent)


@dataclass
class IntegrationEventHandler(ABC, Generic[EventType]):
    @abc.abstractmethod
    async def handle(self, event: EventType) -> None:
        pass
