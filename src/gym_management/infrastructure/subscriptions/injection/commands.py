from dependency_injector import containers, providers

from src.gym_management.application.gyms.commands.create_gym import CreateGymHandler
from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscriptionHandler
from src.gym_management.infrastructure.admins.injection.repository import AdminsRepositoryContainer
from src.gym_management.infrastructure.subscriptions.injection.repository import SubscriptionsRepositoryContainer


class SubscriptionCommandsContainer(containers.DeclarativeContainer):
    admins_repository = providers.Container(AdminsRepositoryContainer)
    subscriptions_repository = providers.Container(SubscriptionsRepositoryContainer)

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admins_repository=admins_repository.repository,
        subscriptions_repository=subscriptions_repository.repository,
    )

    create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscriptions_repository=admins_repository.repository,
    )
