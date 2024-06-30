from dependency_injector import containers, providers

from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscriptionHandler
from src.gym_management.infrastructure.dependency_injection import InfrastructureContainer


class ApplicationContainer(containers.DeclarativeContainer):
    infrastructure_container = providers.Container(InfrastructureContainer)

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler, admins_repository=infrastructure_container.admins_repository
    )
