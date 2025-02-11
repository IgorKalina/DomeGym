from dependency_injector import containers, providers

from src.gym_management.application.gym.queries.get_gym import GetGym, GetGymHandler
from src.gym_management.application.room.queries.list_rooms import ListRooms, ListRoomsHandler
from src.gym_management.application.subscription.queries.get_subscription import GetSubscriptionHandler
from src.gym_management.application.subscription.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class QueryContainer(containers.DeclarativeContainer):
    repository_container = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    get_subscription_handler = providers.Factory(
        GetSubscriptionHandler, subscription_repository=repository_container.subscription_repository
    )
    list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler, subscription_repository=repository_container.subscription_repository
    )
    get_gym_handler = providers.Factory(
        GetGymHandler,
        get_subscription_handler=get_subscription_handler,
        gym_repository=repository_container.gym_repository,
    )
    list_rooms_handler = providers.Factory(
        ListRoomsHandler,
        get_gym_handler=get_gym_handler,
        room_repository=repository_container.room_repository,
    )

    queries = providers.Dict(
        {
            # Subscription
            ListSubscriptions: list_subscriptions_handler,
            # Gym
            GetGym: get_gym_handler,
            # Room
            ListRooms: list_rooms_handler,
        },
    )
