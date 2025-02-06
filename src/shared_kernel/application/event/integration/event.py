import abc
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

__all__ = ["IntegrationEvent", "IntegrationEventHandler", "EventType"]


class IntegrationEvent(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


EventType = TypeVar("EventType", bound=IntegrationEvent)


@dataclass
class IntegrationEventHandler(ABC, Generic[EventType]):
    @abc.abstractmethod
    async def handle(self, event: EventType) -> None:
        pass
