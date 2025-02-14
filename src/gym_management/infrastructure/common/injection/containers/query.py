from dependency_injector import containers, providers

from src.gym_management.application.admin.queries.get_admin import GetAdmin, GetAdminHandler
from src.gym_management.application.gym.queries.get_gym import GetGym, GetGymHandler
from src.gym_management.application.gym.queries.list_gyms import ListGyms, ListGymsHandler
from src.gym_management.application.room.queries.get_room import GetRoom, GetRoomHandler
from src.gym_management.application.room.queries.list_rooms import ListRooms, ListRoomsHandler
from src.gym_management.application.subscription.queries.get_subscription import GetSubscription, GetSubscriptionHandler
from src.gym_management.application.subscription.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus


class QueryContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    query_bus: QueryBus = providers.Dependency(instance_of=QueryBus)

    # Admin
    get_admin_handler = providers.Factory(
        GetAdminHandler,
        admin_repository=repository_container.admin_repository,
    )

    # Subscription
    get_subscription_handler = providers.Factory(
        GetSubscriptionHandler, subscription_repository=repository_container.subscription_repository
    )
    list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler, subscription_repository=repository_container.subscription_repository
    )

    # Gym
    get_gym_handler = providers.Factory(
        GetGymHandler,
        gym_repository=repository_container.gym_repository,
        subscription_repository=repository_container.subscription_repository,
    )
    list_gyms_handler = providers.Factory(
        ListGymsHandler,
        gym_repository=repository_container.gym_repository,
    )

    # Room
    list_rooms_handler = providers.Factory(
        ListRoomsHandler,
        room_repository=repository_container.room_repository,
        gym_repository=repository_container.gym_repository,
        subscription_repository=repository_container.subscription_repository,
    )
    get_room_handler = providers.Factory(
        GetRoomHandler,
        room_repository=repository_container.room_repository,
        gym_repository=repository_container.gym_repository,
    )

    queries = providers.Dict(
        {
            # Admin
            GetAdmin: get_admin_handler,
            # Subscription
            GetSubscription: get_subscription_handler,
            ListSubscriptions: list_subscriptions_handler,
            # Gym
            GetGym: get_gym_handler,
            ListGyms: list_gyms_handler,
            # Room
            GetRoom: get_room_handler,
            ListRooms: list_rooms_handler,
        },
    )
