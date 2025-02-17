from dependency_injector import containers, providers

from src.gym_management.application.gym.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.application.gym.domain_events.gym_removed_handler import GymRemovedHandler
from src.gym_management.application.room.domain_events.room_added_handler import RoomAddedHandler
from src.gym_management.application.room.domain_events.room_removed_handler import RoomRemovedHandler
from src.gym_management.application.room.domain_events.some_event_handler import SomeEventHandler
from src.gym_management.application.subscription.domain_events.subscription_set_handler import SubscriptionSetHandler
from src.gym_management.application.subscription.domain_events.subscription_unset_handler import (
    SubscriptionUnsetHandler,
)
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus


class DomainEventContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    domain_event_bus = providers.Dependency(instance_of=DomainEventBus)

    # Subscription
    subscription_set_handler = providers.Factory(
        SubscriptionSetHandler,
        subscription_repository=repository_container.subscription_repository,
        domain_event_bus=domain_event_bus,
    )
    subscription_unset_handler = providers.Factory(
        SubscriptionUnsetHandler,
        gym_repository=repository_container.gym_repository,
        subscription_repository=repository_container.subscription_repository,
        domain_event_bus=domain_event_bus,
    )

    # Gym
    gym_added_handler = providers.Factory(
        GymAddedEventHandler, gym_repository=repository_container.gym_repository, domain_event_bus=domain_event_bus
    )
    gym_removed_handler = providers.Factory(
        GymRemovedHandler,
        room_repository=repository_container.room_repository,
        gym_repository=repository_container.gym_repository,
        domain_event_bus=domain_event_bus,
    )

    # Room
    room_added_handler = providers.Factory(
        RoomAddedHandler,
        room_repository=repository_container.room_repository,
    )
    room_removed_handler = providers.Factory(
        RoomRemovedHandler,
        room_repository=repository_container.room_repository,
    )

    # Other
    some_event_handler = providers.Factory(SomeEventHandler)

    domain_events = providers.Dict(
        {
            # Subscription
            SubscriptionSetEvent: providers.List(subscription_set_handler),
            SubscriptionUnsetEvent: providers.List(subscription_unset_handler),
            # Gym
            GymAddedEvent: providers.List(gym_added_handler),
            GymRemovedEvent: providers.List(gym_removed_handler),
            # Room
            RoomAddedEvent: providers.List(room_added_handler),
            RoomRemovedEvent: providers.List(room_removed_handler),
            # Other
            SomeEvent: providers.List(some_event_handler),
        }
    )
