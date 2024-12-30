from dependency_injector import containers, providers

from src.gym_management.infrastructure.admin.repository.repository_memory import AdminMemoryRepository
from src.gym_management.infrastructure.gym.repository.repository_memory import GymMemoryRepository
from src.gym_management.infrastructure.subscription.repository.repository_memory import SubscriptionMemoryRepository


class RepositoryContainer(containers.DeclarativeContainer):
    admin_repository = providers.Singleton(AdminMemoryRepository)
    subscription_repository = providers.Singleton(SubscriptionMemoryRepository)
    gym_repository = providers.Singleton(GymMemoryRepository)
