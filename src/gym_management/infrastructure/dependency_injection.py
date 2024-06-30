from dependency_injector import containers, providers

from src.gym_management.infrastructure.admins.persistence.repositories.memory_repository import AdminsMemoryRepository


class InfrastructureContainer(containers.DeclarativeContainer):
    admins_repository = providers.Singleton(AdminsMemoryRepository)
