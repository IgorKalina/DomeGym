import abc
from abc import ABC
from datetime import datetime, timezone
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["DomainEvent", "DomainEventHandler", "EventType"]


class DomainEvent(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(arbitrary_types_allowed=True)


EventType = TypeVar("EventType", bound=DomainEvent)


class DomainEventHandler(ABC, Generic[EventType]):
    @abc.abstractmethod
    async def handle(self, event: EventType) -> None:
        pass
