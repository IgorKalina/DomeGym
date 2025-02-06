import abc
from abc import abstractmethod

from src.shared_kernel.infrastructure.eventbus.interfaces.broker import EventHandler


class EventSubscriber(abc.ABC):
    @abstractmethod
    async def subscribe(self, handler: EventHandler) -> None:
        pass
