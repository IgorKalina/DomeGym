from dependency_injector import containers, providers

from src.gym_management.application.gyms.commands.create_gym import CreateGymHandler
from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscriptionHandler


class CommandsContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admins_repository=infrastructure.admins_repository,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )

    create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )
