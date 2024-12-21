from dependency_injector import containers, providers

from src.gym_management.infrastructure.admins.repository.repository_memory import AdminsMemoryRepository


class AdminsRepositoryContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(AdminsMemoryRepository)
