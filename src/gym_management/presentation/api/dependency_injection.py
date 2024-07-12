from dependency_injector import containers, providers

from src.common.mediator.interfaces import IMediator
from src.gym_management.application.dependency_injection import ApplicationContainer


class DependencyContainer(containers.DeclarativeContainer):
    app = providers.Container(ApplicationContainer)

    @classmethod
    def get_mediator(cls) -> IMediator:
        return cls.app.mediator.mediator
