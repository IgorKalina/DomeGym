from src.gym_management.infrastructure.common.eventbus.rabbitmq.options import (
    RabbitmqExchangeOptions,
    RabbitmqQueueOptions,
    RabbitmqTopicOptions,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer


async def setup_topics(di_container: DiContainer) -> None:
    config = di_container.config
    broker = await di_container.eventbus_container.broker()
    for queue in config.rabbitmq.queues:
        exchange_options = RabbitmqExchangeOptions(name=queue.exchange_name)
        queue_options = RabbitmqQueueOptions(
            name=queue.queue_name, exchange_name=queue.exchange_name, routing_key=queue.routing_key
        )
        topic_options = RabbitmqTopicOptions(exchange=exchange_options, queue=queue_options)
        await broker.create_topic(topic_options)
