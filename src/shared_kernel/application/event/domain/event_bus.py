import abc
from typing import Type

from src.shared_kernel.domain.common.event import DomainEvent, DomainEventHandler


class DomainEventBus(abc.ABC):
    async def publish(self, event: DomainEvent) -> None:
        pass

    async def subscribe(self, event: Type[DomainEvent], handler: DomainEventHandler) -> None:
        pass
