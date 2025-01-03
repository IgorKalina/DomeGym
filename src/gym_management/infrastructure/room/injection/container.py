from dependency_injector import containers, providers

from src.gym_management.application.room.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.application.room.domain_events.some_event_handler import SomeEventHandler
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class RoomContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    domain_events = providers.Dict(
        {
            GymAddedEvent: providers.Factory(GymAddedEventHandler, eventbus=domain_eventbus),
            SubscriptionSetEvent: providers.Factory(GymAddedEventHandler, eventbus=domain_eventbus),
            SomeEvent: providers.Factory(SomeEventHandler),
        }
    )
