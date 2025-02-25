import abc
from abc import abstractmethod
from typing import Generic, TypeVar

from src.gym_management.application.common.dto.repository import DomainEventDB
from src.shared_kernel.application.event.integration.event import IntegrationEvent
from src.shared_kernel.domain.common.event import DomainEvent

EventType = TypeVar("EventType", bound=DomainEvent | IntegrationEvent | DomainEventDB)


class EventPublisher(abc.ABC, Generic[EventType]):
    @abstractmethod
    async def publish(self, event: EventType) -> None:
        pass
