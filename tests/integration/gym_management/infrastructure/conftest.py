import pytest

from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.eventbus.rabbitmq.options import (
    RabbitmqExchangeOptions,
    RabbitmqQueueOptions,
    RabbitmqTopicOptions,
)
from src.gym_management.infrastructure.injection.main import DiContainer
from tests.common.gym_management.common.config.config import ConfigTest


@pytest.fixture
async def broker(di_container: DiContainer) -> RabbitmqEventBroker:
    return await di_container.eventbus_container.broker()


@pytest.fixture(autouse=True)
async def create_topics(broker: RabbitmqEventBroker, config: ConfigTest) -> None:
    for queue in config.rabbitmq.queues:
        exchange_options = RabbitmqExchangeOptions(name=queue.exchange_name)
        queue_options = RabbitmqQueueOptions(
            name=queue.queue_name, exchange_name=queue.exchange_name, routing_key=queue.routing_key
        )
        topic_options = RabbitmqTopicOptions(exchange=exchange_options, queue=queue_options)
        await broker.create_topic(topic_options)
