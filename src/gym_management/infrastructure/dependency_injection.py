from dependency_injector import containers, providers

from src.gym_management.infrastructure.admins.persistence.repositories.memory_repository import AdminsMemoryRepository
from src.gym_management.infrastructure.subscriptions.persistence.repositories.memory_repository import (
    SubscriptionsMemoryRepository,
)


class InfrastructureContainer(containers.DeclarativeContainer):
    admins_repository = providers.Singleton(AdminsMemoryRepository)
    subscriptions_repository = providers.Singleton(SubscriptionsMemoryRepository)
