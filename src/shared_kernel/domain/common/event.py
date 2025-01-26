import abc
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Generic, TypeVar

__all__ = ["DomainEvent", "DomainEventHandler", "EventType"]


@dataclass(kw_only=True, frozen=True)
class DomainEvent(abc.ABC):
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


EventType = TypeVar("EventType", bound=DomainEvent)


class DomainEventHandler(ABC, Generic[EventType]):
    @abc.abstractmethod
    async def handle(self, event: EventType) -> None:
        pass
