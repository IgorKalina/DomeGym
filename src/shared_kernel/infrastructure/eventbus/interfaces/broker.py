import abc
from abc import abstractmethod
from typing import Awaitable, Callable

from src.gym_management.infrastructure.eventbus.rabbitmq.options import PublishOptions, SubscribeOptions
from src.shared_kernel.infrastructure.eventbus.interfaces.event import Event
from src.shared_kernel.infrastructure.eventbus.interfaces.options import BrokerOptions, TopicOptions

EventHandler = Callable[[Event], Awaitable[None]]


class EventBroker(abc.ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def create_topic(self, options: TopicOptions) -> None:
        pass

    @property
    @abstractmethod
    def options(self) -> BrokerOptions:
        pass

    @abstractmethod
    async def publish(self, event: Event, options: PublishOptions) -> None:
        pass

    @abstractmethod
    async def subscribe(self, handler: EventHandler, options: SubscribeOptions) -> None:
        pass
