import logging
from types import TracebackType
from typing import Self, Type

from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker.connection import RabbitmqConnection
from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker.exchange import RabbitmqExchangePool
from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker.queue import RabbitmqQueuePool
from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker.subscriber import RabbitmqSubscriberPool
from src.gym_management.infrastructure.common.eventbus.rabbitmq.dto.event import RabbitmqEvent
from src.gym_management.infrastructure.common.eventbus.rabbitmq.options import (
    RabbitmqBrokerOptions,
    RabbitmqPublishOptions,
    RabbitmqSubscribeOptions,
    RabbitmqTopicOptions,
)
from src.shared_kernel.infrastructure.eventbus.interfaces.broker import EventBroker, EventHandler

logger = logging.getLogger(__name__)


class RabbitmqEventBroker(EventBroker):
    def __init__(self, options: RabbitmqBrokerOptions) -> None:
        self.__options = options

        self.__connection = RabbitmqConnection(self.__options)
        self.__exchange_pool = RabbitmqExchangePool(self.__connection)
        self.__queue_pool = RabbitmqQueuePool(connection=self.__connection, exchange=self.__exchange_pool)
        self.__subscriber_pool = RabbitmqSubscriberPool(connection=self.__connection, queue=self.__queue_pool)

    @property
    def connection(self) -> RabbitmqConnection:
        return self.__connection

    @property
    def options(self) -> RabbitmqBrokerOptions:
        return self.__options.model_copy()

    async def connect(self) -> None:
        await self.__connection.establish()

    async def disconnect(self) -> None:
        await self.__subscriber_pool.shutdown_subscribers()
        self.__exchange_pool.clear_cache()
        self.__queue_pool.clear_cache()
        await self.__connection.close()
        logger.debug(f"Disconnected from RabbitMQ by URL: {self.__options.get_url()}")

    async def create_topic(self, options: RabbitmqTopicOptions) -> None:
        await self.__exchange_pool.add_exchange(options.exchange)
        await self.__queue_pool.add_queue(options.queue)

    async def publish(self, event: RabbitmqEvent, options: RabbitmqPublishOptions) -> None:
        async with self.__connection.channel():
            exchange = await self.__exchange_pool.get(options.exchange_name)

            logger.info(f"Publishing event id '{event.id}' to '{options.routing_key}' routing key")
            await exchange.publish(
                message=event.to_pika_message(),
                routing_key=options.routing_key,
            )
            logger.info("Event was published")

    async def subscribe(self, handler: EventHandler, options: RabbitmqSubscribeOptions) -> None:
        await self.__subscriber_pool.add_subscriber(handler, options)

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
