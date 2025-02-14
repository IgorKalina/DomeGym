from dependency_injector import containers, providers

from src.gym_management.application.gym.domain_events.subscription_unset_handler import SubscriptionUnsetHandler
from src.gym_management.application.room.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.application.room.domain_events.gym_removed_handler import GymRemovedHandler
from src.gym_management.application.room.domain_events.some_event_handler import SomeEventHandler
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus


class DomainEventContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    domain_event_bus = providers.Dependency(instance_of=DomainEventBus)

    gym_added_handler = providers.Factory(GymAddedEventHandler, domain_event_bus=domain_event_bus)
    some_event_handler = providers.Factory(SomeEventHandler)
    subscription_unset_handler = providers.Factory(
        SubscriptionUnsetHandler,
        gym_repository=repository_container.gym_repository,
        domain_event_bus=domain_event_bus,
    )
    gym_removed_handler = providers.Factory(
        GymRemovedHandler,
        room_repository=repository_container.room_repository,
        domain_event_bus=domain_event_bus,
    )

    domain_events = providers.Dict(
        {
            # Subscription
            SubscriptionSetEvent: providers.List(gym_added_handler),
            SubscriptionUnsetEvent: providers.List(subscription_unset_handler),
            # Gym
            GymAddedEvent: providers.List(gym_added_handler),
            GymRemovedEvent: providers.List(gym_removed_handler),
            # Other
            SomeEvent: providers.List(some_event_handler),
        }
    )
