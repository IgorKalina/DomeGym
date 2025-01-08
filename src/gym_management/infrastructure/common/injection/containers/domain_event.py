from dependency_injector import containers, providers

from src.gym_management.application.room.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.application.room.domain_events.some_event_handler import SomeEventHandler
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class DomainEventContainer(containers.DeclarativeContainer):
    repository = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    __gym_added_handler = providers.Factory(GymAddedEventHandler, eventbus=domain_eventbus)
    __some_event_handler = providers.Factory(SomeEventHandler)

    domain_events = providers.Dict(
        {
            GymAddedEvent: providers.List(__gym_added_handler),
            SubscriptionSetEvent: providers.List(__gym_added_handler),
            SomeEvent: providers.List(__some_event_handler),
        }
    )
