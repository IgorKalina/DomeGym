from dependency_injector import containers, providers

from src.gym_management.application.gym.domain_events.subscription_removed_handler import SubscriptionRemovedHandler
from src.gym_management.application.room.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.application.room.domain_events.gym_removed_handler import GymRemovedHandler
from src.gym_management.application.room.domain_events.some_event_handler import SomeEventHandler
from src.gym_management.domain.admin.events.subscription_removed_event import SubscriptionRemovedEvent
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class DomainEventContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    gym_added_handler = providers.Factory(GymAddedEventHandler, eventbus=domain_eventbus)
    some_event_handler = providers.Factory(SomeEventHandler)
    subscription_removed_handler = providers.Factory(
        SubscriptionRemovedHandler,
        gym_repository=repository_container.gym_repository,
        room_repository=repository_container.room_repository,
        eventbus=domain_eventbus,
    )
    gym_removed_handler = providers.Factory(
        GymRemovedHandler,
        room_repository=repository_container.room_repository,
        eventbus=domain_eventbus,
    )

    domain_events = providers.Dict(
        {
            GymAddedEvent: providers.List(gym_added_handler),
            SubscriptionSetEvent: providers.List(gym_added_handler),
            SomeEvent: providers.List(some_event_handler),
            SubscriptionRemovedEvent: providers.List(subscription_removed_handler),
            GymRemovedEvent: providers.List(gym_removed_handler),
        }
    )
