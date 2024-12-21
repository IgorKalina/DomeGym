from dependency_injector import containers, providers

from src.gym_management.infrastructure.admins.repository.repository_memory import AdminsMemoryRepository
from src.gym_management.infrastructure.subscriptions.repository.repository_memory import SubscriptionsMemoryRepository


class InfrastructureContainer(containers.DeclarativeContainer):
    admins_repository = providers.Singleton(AdminsMemoryRepository)
    subscriptions_repository = providers.Singleton(SubscriptionsMemoryRepository)
