import asyncio
import contextlib
import logging
import uuid
from typing import List

import aio_pika
from aio_pika.abc import AbstractRobustQueue

from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqConnection, RabbitmqQueuePool
from src.gym_management.infrastructure.eventbus.rabbitmq.dto.event import RabbitmqEvent
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqSubscribeOptions
from src.shared_kernel.infrastructure.eventbus.interfaces.broker import EventHandler

logger = logging.getLogger(__name__)


class RabbitmqSubscriberPool:
    def __init__(self, connection: RabbitmqConnection, queue: RabbitmqQueuePool) -> None:
        self.__connection = connection
        self.__queue_pool = queue
        self.__subscriber_tasks: List[asyncio.Task] = []

    async def add_subscriber(self, handler: EventHandler, options: RabbitmqSubscribeOptions) -> None:
        logger.info(f"Subscribing to '{options.queue_name}' queue")
        queue = await self.__queue_pool.get(options.queue_name)
        task = asyncio.create_task(self.__subscribe(queue=queue, handler=handler, options=options))
        self.__subscriber_tasks.append(task)

    async def shutdown_subscribers(self) -> None:
        for task in self.__subscriber_tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task  # Wait for it to properly stop
        self.__subscriber_tasks = []

    async def __subscribe(
        self, queue: AbstractRobustQueue, handler: EventHandler, options: RabbitmqSubscribeOptions
    ) -> None:
        consumer_tag = f"{options.queue_name}-{uuid.uuid4()}"
        logger.info(f"Consuming messages from queue: {options.queue_name} with tag: {consumer_tag}")
        try:
            async with self.__connection.channel():
                await queue.consume(handler, consumer_tag=consumer_tag)
                await asyncio.Future()  # Keeps the consumer running
        except asyncio.CancelledError:
            logger.info("Consumer task has been cancelled.")
            # Handle graceful task cancellation here (e.g., finishing in-progress message)
        finally:
            logger.info("Consumer stopped gracefully.")

    @staticmethod
    async def __handle(event: aio_pika.IncomingMessage, handler: EventHandler) -> None:
        event = RabbitmqEvent.from_pika_message(event)
        await handler(event)
