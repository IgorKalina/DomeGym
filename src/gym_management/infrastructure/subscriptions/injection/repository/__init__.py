from dependency_injector import containers, providers

from src.gym_management.infrastructure.subscriptions.repository.repository_memory import SubscriptionsMemoryRepository


class SubscriptionsRepositoryContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(SubscriptionsMemoryRepository)
