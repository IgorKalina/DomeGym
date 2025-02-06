import logging
from typing import Dict

from aio_pika.abc import AbstractRobustQueue

from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqConnection, RabbitmqExchangePool
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqQueueOptions

logger = logging.getLogger(__name__)


class RabbitmqQueuePool:
    def __init__(self, connection: RabbitmqConnection, exchange: RabbitmqExchangePool) -> None:
        self.__connection = connection
        self.__exchange = exchange

        self.__queues: Dict[str, AbstractRobustQueue] = {}

    async def add(self, options: RabbitmqQueueOptions) -> None:
        exchange = await self.__exchange.get(options.exchange_name)
        queue = await self.__connection.channel.declare_queue(name=options.name, durable=options.durable)
        await queue.bind(exchange=exchange, routing_key=options.routing_key)
        self.__queues[options.name] = queue
        logger.info(
            f"Declared queue: {options.name} (bound to {options.exchange_name} with key '{options.routing_key}')"
        )

    async def get(self, name: str) -> AbstractRobustQueue:
        cached_queue = self.__queues.get(name)
        if cached_queue is None:
            exchange = await self.__fetch_queue(name)
            self.__queues[name] = exchange
        else:
            exchange = cached_queue
        return exchange

    async def __fetch_queue(self, name: str) -> AbstractRobustQueue:
        # todo: add try-except in case queue does not exist
        return await self.__connection.channel.get_queue(name)
