from dependency_injector import containers, providers

from src.gym_management.application.subscriptions.queries.list_subscriptions import ListSubscriptionsHandler


class QueriesContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )
