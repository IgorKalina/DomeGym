import abc
from abc import abstractmethod

from src.shared_kernel.infrastructure.eventbus.interfaces.broker import Event


class EventPublisher(abc.ABC):
    @abstractmethod
    async def publish(self, event: Event) -> None:
        pass
