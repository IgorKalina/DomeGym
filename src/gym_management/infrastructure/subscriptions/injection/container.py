from dependency_injector import containers, providers

from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.application.subscriptions.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
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

    queries = providers.Dict(
        {
            ListSubscriptions: providers.Factory(
                ListSubscriptionsHandler, subscriptions_repository=repositories.subscriptions_repository
            )
        }
    )
