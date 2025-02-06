import logging
from typing import Dict

from aio_pika.abc import AbstractRobustExchange
from aiormq import ChannelNotFoundEntity

from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqConnection
from src.gym_management.infrastructure.eventbus.rabbitmq.exceptions import ExchangeDoesNotExistError
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqExchangeOptions

logger = logging.getLogger(__name__)


class RabbitmqExchangePool:
    def __init__(self, connection: RabbitmqConnection) -> None:
        self.__connection = connection

        self.__exchanges: Dict[str, AbstractRobustExchange] = {}

    async def add(self, options: RabbitmqExchangeOptions) -> None:
        exchange = await self.__connection.channel.declare_exchange(
            name=options.name, type=options.type, durable=options.durable
        )
        self.__exchanges[options.name] = exchange
        logger.info(f"Added exchange: {options.name}")

    async def get(self, name: str) -> AbstractRobustExchange:
        cached_exchange = self.__exchanges.get(name)
        if cached_exchange is None:
            exchange = await self.__fetch_exchange(name)
            self.__exchanges[name] = exchange
        else:
            exchange = cached_exchange
        return exchange

    async def __fetch_exchange(self, name: str) -> AbstractRobustExchange:
        try:
            exchange = await self.__connection.channel.get_exchange(name)
        except ChannelNotFoundEntity:
            raise ExchangeDoesNotExistError(exchange_name=name, broker_url=self.__connection.options.get_url())
        return exchange
