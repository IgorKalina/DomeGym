from dependency_injector import containers, providers

from src.gym_management.application.gym.queries.get_gym import GetGym, GetGymHandler
from src.gym_management.application.subscription.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class QueryContainer(containers.DeclarativeContainer):
    repository = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    __list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler, subscription_repository=repository.subscription_repository
    )
    __get_gym_handler = providers.Factory(
        GetGymHandler,
        subscription_repository=repository.subscription_repository,
        gym_repository=repository.gym_repository,
    )

    queries = providers.Dict(
        {ListSubscriptions: __list_subscriptions_handler, GetGym: __get_gym_handler},
    )
