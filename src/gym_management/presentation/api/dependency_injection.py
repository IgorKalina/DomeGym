from dependency_injector import containers, providers

from src.gym_management.application.dependency_injection import ApplicationContainer
from src.gym_management.infrastructure.dependency_injection import InfrastructureContainer
from src.shared_kernel.application.mediator.interfaces import IMediator


class DependencyContainer(containers.DeclarativeContainer):
    infrastructure = providers.Container(InfrastructureContainer)
    app = providers.Container(
        ApplicationContainer,
        infrastructure_container=infrastructure,
    )

    @classmethod
    def get_mediator(cls) -> IMediator:
        return cls.app.mediator.mediator  # type: ignore
