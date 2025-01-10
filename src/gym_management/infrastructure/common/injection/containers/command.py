from dependency_injector import containers, providers

from src.gym_management.application.gym.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.application.subscription.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class CommandContainer(containers.DeclarativeContainer):
    repository_container = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admin_repository=repository_container.admin_repository,
        subscription_repository=repository_container.subscription_repository,
        eventbus=domain_eventbus,
    )
    create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscription_repository=repository_container.subscription_repository,
        gym_repository=repository_container.gym_repository,
        eventbus=domain_eventbus,
    )

    commands = providers.Dict(
        {CreateSubscription: create_subscription_handler, CreateGym: create_gym_handler},
    )
