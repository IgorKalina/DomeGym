from dependency_injector import providers

from src.gym_management.infrastructure.common.injection.containers.eventbus.base import EventbusContainer


class EventBusMemoryContainer(EventbusContainer):
    broker = providers.Callable(None)
    domain_event_publisher = providers.Callable(None)
