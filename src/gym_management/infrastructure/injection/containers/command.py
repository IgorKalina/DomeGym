from dependency_injector import containers, providers

from src.gym_management.application.gym.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.application.room.commands.create_room import CreateRoom, CreateRoomHandler
from src.gym_management.application.subscription.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.application.subscription.commands.remove_subscription import (
    RemoveSubscription,
    RemoveSubscriptionHandler,
)
from src.gym_management.infrastructure.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus


class CommandContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    domain_eventbus: DomainEventBus = providers.Dependency(instance_of=DomainEventBus)
    query_bus: QueryBus = providers.Dependency(instance_of=QueryBus)

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admin_repository=repository_container.admin_repository,
        subscription_repository=repository_container.subscription_repository,
        eventbus=domain_eventbus,
    )
    create_gym_handler = providers.Factory(
        CreateGymHandler,
        query_bus=query_bus,
        gym_repository=repository_container.gym_repository,
        eventbus=domain_eventbus,
    )

    create_room_handler = providers.Factory(
        CreateRoomHandler,
        query_bus=query_bus,
        room_repository=repository_container.room_repository,
        eventbus=domain_eventbus,
    )
    remove_subscription_handler = providers.Factory(
        RemoveSubscriptionHandler,
        query_bus=query_bus,
        admin_repository=repository_container.admin_repository,
        subscription_repository=repository_container.subscription_repository,
        eventbus=domain_eventbus,
    )

    commands = providers.Dict(
        {
            # Subscription
            CreateSubscription: create_subscription_handler,
            RemoveSubscription: remove_subscription_handler,
            # Gym
            CreateGym: create_gym_handler,
            # Room
            CreateRoom: create_room_handler,
        },
    )
