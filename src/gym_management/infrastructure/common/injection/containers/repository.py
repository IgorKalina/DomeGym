from dependency_injector import containers, providers

from src.gym_management.infrastructure.admin.repository.repository_memory import AdminsMemoryRepository
from src.gym_management.infrastructure.subscription.repository.repository_memory import SubscriptionsMemoryRepository


class RepositoryContainer(containers.DeclarativeContainer):
    admins_repository = providers.Singleton(AdminsMemoryRepository)
    subscriptions_repository = providers.Singleton(SubscriptionsMemoryRepository)
