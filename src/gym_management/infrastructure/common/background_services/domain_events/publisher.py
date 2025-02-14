from src.gym_management.infrastructure.common.background_services.domain_events.mappers import (
    domain_event_to_rabbitmq_event,
)
from src.gym_management.infrastructure.common.eventbus.rabbitmq.broker import RabbitmqEventBroker
from src.gym_management.infrastructure.common.eventbus.rabbitmq.options import RabbitmqPublishOptions
from src.shared_kernel.domain.common.event import DomainEvent
from src.shared_kernel.infrastructure.eventbus.interfaces.publisher import EventPublisher


class DomainEventPublisher(EventPublisher[DomainEvent]):
    def __init__(self, broker: RabbitmqEventBroker) -> None:
        self.__broker = broker
        self.__publish_options = RabbitmqPublishOptions(
            exchange_name="domain_events",
            routing_key="domain_events",
        )

    async def publish(self, event: DomainEvent) -> None:
        rabbitmq_event = domain_event_to_rabbitmq_event(event)
        await self.__broker.publish(rabbitmq_event, options=self.__publish_options)
