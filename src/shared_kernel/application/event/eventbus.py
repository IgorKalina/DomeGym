import abc
from typing import List, Type

from src.shared_kernel.domain.event import DomainEvent, DomainEventHandler


class EventBus(abc.ABC):
    async def publish(self, events: List[DomainEvent]) -> None:
        pass

    async def subscribe(self, event: Type[DomainEvent], handler: DomainEventHandler) -> None:
        pass

    async def process_events(self) -> None:
        pass
