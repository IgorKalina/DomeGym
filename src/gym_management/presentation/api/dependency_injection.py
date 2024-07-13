from dependency_injector import containers, providers

from src.common.mediator.interfaces import IMediator
from src.gym_management.application.dependency_injection import ApplicationContainer
from src.gym_management.infrastructure.dependency_injection import InfrastructureContainer


class DependencyContainer(containers.DeclarativeContainer):
    infrastructure = providers.Container(InfrastructureContainer)
    app = providers.Container(
        ApplicationContainer,
        infrastructure_container=infrastructure,
    )

    @classmethod
    def get_mediator(cls) -> IMediator:
        return cls.app.mediator.mediator  # type: ignore
