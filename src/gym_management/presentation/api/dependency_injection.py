from dependency_injector import containers, providers

from src.gym_management.application.dependency_injection import ApplicationContainer


class DependencyContainer(containers.DeclarativeContainer):
    app_container = providers.Container(ApplicationContainer)
