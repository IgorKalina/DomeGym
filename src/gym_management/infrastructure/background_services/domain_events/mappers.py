from src.gym_management.infrastructure.background_services.domain_events.event_registry.domain_event_type import (
    DomainEventType,
)
from src.gym_management.infrastructure.background_services.domain_events.event_registry.registry import (
    DomainEventRegistry,
)
from src.gym_management.infrastructure.eventbus.rabbitmq.dto.event import RabbitmqEvent
from src.shared_kernel.domain.common.event import DomainEvent


def rabbitmq_event_to_domain_event(event: RabbitmqEvent) -> DomainEvent:
    event_type = DomainEventType(event.event_type)
    domain_event_class = DomainEventRegistry().get_event_class(event_type)
    return domain_event_class(**event.data)


def domain_event_to_rabbitmq_event(event: DomainEvent) -> RabbitmqEvent:
    return RabbitmqEvent(
        data=event.model_dump(),
        event_type=DomainEventRegistry().get_event_type(event),
    )
