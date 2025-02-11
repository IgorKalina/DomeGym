from dependency_injector import containers, providers

from src.gym_management.application.gym.queries.get_gym import GetGym, GetGymHandler
from src.gym_management.application.room.queries.list_rooms import ListRooms, ListRoomsHandler
from src.gym_management.application.subscription.queries.get_subscription import GetSubscription, GetSubscriptionHandler
from src.gym_management.application.subscription.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.gym_management.infrastructure.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker


class QueryContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    domain_eventbus: DomainEventBus = providers.Dependency(instance_of=DomainEventBus)
    query_invoker: QueryInvoker = providers.Dependency(instance_of=QueryInvoker)

    get_subscription_handler = providers.Factory(
        GetSubscriptionHandler, subscription_repository=repository_container.subscription_repository
    )
    list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler, subscription_repository=repository_container.subscription_repository
    )
    get_gym_handler = providers.Factory(
        GetGymHandler,
        query_invoker=query_invoker,
        gym_repository=repository_container.gym_repository,
    )
    list_rooms_handler = providers.Factory(
        ListRoomsHandler,
        query_invoker=query_invoker,
        room_repository=repository_container.room_repository,
    )

    queries = providers.Dict(
        {
            # Subscription
            ListSubscriptions: list_subscriptions_handler,
            GetSubscription: get_subscription_handler,
            # Gym
            GetGym: get_gym_handler,
            # Room
            ListRooms: list_rooms_handler,
        },
    )
