from typing import AsyncGenerator

from dependency_injector import providers

from src.gym_management.infrastructure.common.config.rabbitmq import RabbitmqConfig
from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.common.eventbus.rabbitmq.options import RabbitmqBrokerOptions
from src.gym_management.infrastructure.common.injection.containers.eventbus.base import EventbusContainer


async def _init_rabbitmq_event_broker(config: RabbitmqConfig) -> AsyncGenerator[RabbitmqEventBroker, None]:
    options = RabbitmqBrokerOptions(
        user=config.user.name,
        password=config.user.password.get_secret_value(),
        host=config.host,
        port=config.port,
    )
    async with RabbitmqEventBroker(options) as broker:
        yield broker


class EventbusRabbitmqContainer(EventbusContainer):
    config: providers.Dependency[RabbitmqConfig] = providers.Dependency()

    broker = providers.Resource(_init_rabbitmq_event_broker, config=config)
