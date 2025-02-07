import logging
from typing import Dict

from aio_pika.abc import AbstractRobustQueue
from aiormq import ChannelNotFoundEntity

from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqConnection, RabbitmqExchangePool
from src.gym_management.infrastructure.eventbus.rabbitmq.exceptions import QueueDoesNotExistError
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqQueueOptions

logger = logging.getLogger(__name__)


class RabbitmqQueuePool:
    def __init__(self, connection: RabbitmqConnection, exchange: RabbitmqExchangePool) -> None:
        self.__connection = connection
        self.__exchange_pool = exchange

        self.__queues: Dict[str, AbstractRobustQueue] = {}

    async def add_queue(self, options: RabbitmqQueueOptions) -> None:
        exchange = await self.__exchange_pool.get(options.exchange_name)
        async with self.__connection.channel() as channel:
            queue = await channel.declare_queue(name=options.name, durable=options.durable)
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

    def clear_cache(self) -> None:
        self.__queues = {}

    async def __fetch_queue(self, name: str) -> AbstractRobustQueue:
        try:
            async with self.__connection.channel() as channel:
                queue = await channel.get_queue(name)
        except ChannelNotFoundEntity as err:
            if f"no queue '{name}'" in str(err):
                raise QueueDoesNotExistError(queue_name=name, broker_url=self.__connection.options.get_url())
            raise err
        return queue
