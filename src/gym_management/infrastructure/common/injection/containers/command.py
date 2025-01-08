from dependency_injector import containers, providers

from src.gym_management.application.gym.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.application.subscription.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class CommandContainer(containers.DeclarativeContainer):
    repository = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    __create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admin_repository=repository.admin_repository,
        subscription_repository=repository.subscription_repository,
        eventbus=domain_eventbus,
    )
    __create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscription_repository=repository.subscription_repository,
        gym_repository=repository.gym_repository,
        eventbus=domain_eventbus,
    )

    commands = providers.Dict(
        {CreateSubscription: __create_subscription_handler, CreateGym: __create_gym_handler},
    )
