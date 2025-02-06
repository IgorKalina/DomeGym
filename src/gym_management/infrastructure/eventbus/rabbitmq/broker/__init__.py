import logging
from types import TracebackType
from typing import Self, Type

from src.gym_management.infrastructure.eventbus.rabbitmq.broker.connection import RabbitmqConnection
from src.gym_management.infrastructure.eventbus.rabbitmq.broker.exchange import RabbitmqExchangePool
from src.gym_management.infrastructure.eventbus.rabbitmq.broker.queue import RabbitmqQueuePool
from src.gym_management.infrastructure.eventbus.rabbitmq.broker.subscriber import RabbitmqSubscriberPool
from src.gym_management.infrastructure.eventbus.rabbitmq.dto.event import RabbitmqEvent
from src.gym_management.infrastructure.eventbus.rabbitmq.options import (
    RabbitmqBrokerOptions,
    RabbitmqExchangeOptions,
    RabbitmqPublishOptions,
    RabbitmqQueueOptions,
    RabbitmqSubscribeOptions,
)
from src.shared_kernel.infrastructure.eventbus.interfaces.broker import EventBroker, EventHandler

logger = logging.getLogger(__name__)


class RabbitmqEventBroker(EventBroker):
    def __init__(self, options: RabbitmqBrokerOptions) -> None:
        self.__options = options

        self.__connection = RabbitmqConnection(options)
        self.__exchange_pool = RabbitmqExchangePool(self.__connection)
        self.__queue_pool = RabbitmqQueuePool(connection=self.__connection, exchange=self.__exchange_pool)
        self.__subscriber_pool = RabbitmqSubscriberPool(self.__queue_pool)

    async def connect(self) -> None:
        await self.__connection.establish()

    async def disconnect(self) -> None:
        await self.__subscriber_pool.shutdown_subscribers()
        await self.__connection.close()
        logger.debug(f"Disconnected from RabbitMQ by URL: {self.__options.get_url()}")

    async def declare_exchange(self, options: RabbitmqExchangeOptions) -> None:
        await self.__exchange_pool.add(options)

    async def declare_queue(self, options: RabbitmqQueueOptions) -> None:
        await self.__queue_pool.add(options)

    async def publish(self, event: RabbitmqEvent, options: RabbitmqPublishOptions) -> None:
        exchange = await self.__exchange_pool.get(options.exchange_name)

        logger.info(f"Publishing event id '{event.id}' to '{options.routing_key}' routing key")
        await exchange.publish(
            message=event.to_pika_message(),
            routing_key=options.routing_key,
        )
        logger.info("Event was published")

    async def subscribe(self, handler: EventHandler, options: RabbitmqSubscribeOptions) -> None:
        await self.__subscriber_pool.subscribe(handler, options)

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.disconnect()
