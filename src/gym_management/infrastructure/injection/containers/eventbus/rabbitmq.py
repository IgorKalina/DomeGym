from typing import AsyncGenerator

from dependency_injector import providers

from src.gym_management.infrastructure.background_services.domain_events.publisher import DomainEventPublisher
from src.gym_management.infrastructure.config.rabbitmq import RabbitmqConfig
from src.gym_management.infrastructure.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.eventbus.rabbitmq.options import RabbitmqBrokerOptions
from src.gym_management.infrastructure.injection.containers.eventbus.base import EventbusContainer


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
    domain_event_publisher = providers.Factory(DomainEventPublisher, broker=broker)
