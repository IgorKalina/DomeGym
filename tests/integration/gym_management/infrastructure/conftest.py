import logging
from typing import TYPE_CHECKING, AsyncGenerator

import pytest
from aiormq import ChannelInvalidStateError

from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.eventbus.rabbitmq.exceptions import BrokerNotConnectedError
from src.gym_management.infrastructure.eventbus.rabbitmq.options import (
    RabbitmqExchangeOptions,
    RabbitmqQueueOptions,
    RabbitmqTopicOptions,
)
from src.gym_management.infrastructure.injection.main import DiContainer
from tests.common.gym_management.common.config.config import ConfigTest

if TYPE_CHECKING:
    from aio_pika.abc import AbstractQueue

logger = logging.getLogger(__name__)


@pytest.fixture
async def broker(di_container: DiContainer) -> RabbitmqEventBroker:
    return await di_container.eventbus_container.broker()


async def _create_topics(broker: RabbitmqEventBroker, config: ConfigTest) -> None:
    for queue in config.rabbitmq.queues:
        exchange_options = RabbitmqExchangeOptions(name=queue.exchange_name)
        queue_options = RabbitmqQueueOptions(
            name=queue.queue_name, exchange_name=queue.exchange_name, routing_key=queue.routing_key
        )
        topic_options = RabbitmqTopicOptions(exchange=exchange_options, queue=queue_options)
        await broker.create_topic(topic_options)


async def _purge_topics(broker: RabbitmqEventBroker, config: ConfigTest) -> None:
    try:
        async with broker.connection.channel() as channel:
            for existing_queue in config.rabbitmq.queues:
                queue: AbstractQueue = await channel.get_queue(existing_queue.queue_name)
                await queue.purge()
    except BrokerNotConnectedError:
        logger.warning("Broker connection is already closed. Skip purging messages from queues.")
    except ChannelInvalidStateError:
        logger.warning("Channel is already closed. Skip purging messages from queues.")
    except Exception as e:
        logger.warning(f"Error purging queue '{existing_queue.queue_name}': {e}")


@pytest.fixture(autouse=True)
async def setup_topics(broker: RabbitmqEventBroker, config: ConfigTest) -> AsyncGenerator[None, None]:
    await _create_topics(broker=broker, config=config)
    yield
    await _purge_topics(broker=broker, config=config)
