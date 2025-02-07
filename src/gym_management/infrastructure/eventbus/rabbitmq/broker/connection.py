import logging
from contextlib import asynccontextmanager

import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from aio_pika.pool import Pool

from src.gym_management.infrastructure.eventbus.rabbitmq.exceptions import (
    BrokerAlreadyConnectedError,
    BrokerNotConnectedError,
)
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqBrokerOptions

logger = logging.getLogger(__name__)


class RabbitmqConnection:
    def __init__(self, options: RabbitmqBrokerOptions) -> None:
        self.__options = options
        self.__url = self.__options.get_url(safe=False)

        self.__connection: AbstractRobustConnection | None = None
        self.__channel_pool: Pool[AbstractRobustChannel] | None = None

    @property
    def options(self) -> RabbitmqBrokerOptions:
        return self.__options

    @asynccontextmanager
    async def channel(self) -> AbstractRobustChannel:
        if self.__channel_pool is None:
            raise BrokerNotConnectedError()

        async with self.__channel_pool.acquire() as channel:
            yield channel

    async def establish(self) -> None:
        if self.__connection is not None or self.__channel_pool is not None:
            raise BrokerAlreadyConnectedError()

        self.__connection = await aio_pika.connect_robust(self.__url)
        self.__channel_pool = Pool(self.__create_channel, max_size=10)
        logger.debug(f"Connection to RabbitMQ was established by URL: {self.__url}")

    async def __create_channel(self) -> AbstractRobustChannel:
        if self.__connection is None:
            raise BrokerNotConnectedError()

        return await self.__connection.channel()

    async def close(self) -> None:
        await self.__close_connection()
        await self.__close_channel_pool()

    async def __close_channel_pool(self) -> None:
        if self.__channel_pool is None or self.__channel_pool.is_closed:
            logger.warning("Channel pool has been already closed")
            return

        await self.__channel_pool.close()
        self.__channel_pool = None

    async def __close_connection(self) -> None:
        if self.__connection is None or self.__connection.is_closed:
            logger.warning("Connection has been already closed")
            return

        await self.__connection.close()
        self.__connection = None
