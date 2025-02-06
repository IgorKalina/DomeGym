import logging

import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection

from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqBrokerOptions

logger = logging.getLogger(__name__)


class RabbitmqConnection:
    def __init__(self, options: RabbitmqBrokerOptions) -> None:
        self.__options = options
        self.__url = self.__options.get_url(safe=False)

        self.__connection: AbstractRobustConnection | None = None
        self.__channel: AbstractRobustChannel | None = None

    @property
    def options(self) -> RabbitmqBrokerOptions:
        return self.__options

    @property
    def channel(self) -> AbstractRobustChannel:
        if self.__channel is None:
            # todo: update to more concrete exception
            raise Exception("Channel is None. Did you forget to call '.connect()'?")
        return self.__channel

    async def establish(self) -> None:
        if self.__connection is not None or self.__channel is not None:
            raise Exception("Already connected error")

        self.__connection = await aio_pika.connect_robust(self.__url)
        self.__channel = await self.__connection.channel()
        logger.debug(f"Connection to RabbitMQ was established by URL: {self.__url}")

    async def close(self) -> None:
        await self.__close_channel()
        await self.__close_connection()

    async def __close_channel(self) -> None:
        if self.__channel is None or self.__channel.is_closed:
            logger.warning("Channel has been already closed")
            return

        await self.__channel.close()
        self.__channel = None

    async def __close_connection(self) -> None:
        if self.__connection is None or self.__connection.is_closed:
            logger.warning("Connection has been already closed")
            return

        await self.__connection.close()
        self.__connection = None
