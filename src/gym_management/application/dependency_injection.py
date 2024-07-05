from dependency_injector import containers, providers

from src.gym_management.application.gyms.commands.create_gym import CreateGymHandler
from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscriptionHandler
from src.gym_management.application.subscriptions.queries.list_subscriptions import ListSubscriptionsHandler
from src.gym_management.infrastructure.dependency_injection import InfrastructureContainer


class ApplicationContainer(containers.DeclarativeContainer):
    infrastructure_container = providers.Container(InfrastructureContainer)

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admins_repository=infrastructure_container.admins_repository,
        subscriptions_repository=infrastructure_container.subscriptions_repository,
    )

    list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler,
        subscriptions_repository=infrastructure_container.subscriptions_repository,
    )

    create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscriptions_repository=infrastructure_container.subscriptions_repository,
    )
