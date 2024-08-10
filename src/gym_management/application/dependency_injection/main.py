from dependency_injector import containers, providers

from src.gym_management.application.dependency_injection.containers import (
    CommandsContainer,
    EventsContainer,
    QueriesContainer,
)
from src.gym_management.application.dependency_injection.mediator import init_mediator


class ApplicationContainer(containers.DeclarativeContainer):
    infrastructure_container = providers.DependenciesContainer()

    commands_container = providers.Container(CommandsContainer, infrastructure=infrastructure_container)
    queries_container = providers.Container(QueriesContainer, infrastructure=infrastructure_container)
    events_container = providers.Container(EventsContainer, infrastructure=infrastructure_container)

    mediator = providers.Resource(
        init_mediator,
        commands=commands_container,
        queries=queries_container,
        events=events_container,
    )
