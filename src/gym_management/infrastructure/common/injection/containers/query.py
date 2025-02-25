from typing import Dict

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
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork
from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory


async def _create_query_bus(unit_of_work: UnitOfWork, queries: Dict) -> QueryBusMemory:
    query_bus = QueryBusMemory(unit_of_work=unit_of_work)
    for query, handler in queries.items():
        query_bus.register_query_handler(query, handler)
    return query_bus


class QueryContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()

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

    query_bus: providers.Factory[QueryBusMemory] = providers.Factory(
        _create_query_bus,
        unit_of_work=repository_container.unit_of_work,
        queries=queries,
    )
