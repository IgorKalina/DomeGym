from dependency_injector import containers, providers

from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)


class SubscriptionsContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    commands = providers.Dict(
        {
            CreateSubscription: providers.Factory(
                CreateSubscriptionHandler,
                admins_repository=repositories.admins_repository,
                subscriptions_repository=repositories.subscriptions_repository,
            )
        }
    )
