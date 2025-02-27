from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.injection.containers.command import CommandContainer
from src.gym_management.infrastructure.common.injection.containers.domain_event import DomainEventContainer
from src.gym_management.infrastructure.common.injection.containers.query import QueryContainer
from tests.common.gym_management.common.injection.containers.event_bus_memory_container import EventBusMemoryContainer
from tests.common.gym_management.common.injection.containers.repository_memory_container import (
    RepositoryMemoryContainer,
)


class DiMemoryContainer(containers.DeclarativeContainer):
    # dependencies
    repository_container: RepositoryMemoryContainer = providers.Container(RepositoryMemoryContainer)
    eventbus_container: EventBusMemoryContainer = providers.Container(EventBusMemoryContainer)

    # containers needs to be re-defined to use new dependencies defined
    query_container = providers.Container(
        QueryContainer,
        repository_container=repository_container,
    )
    command_container: CommandContainer = providers.Container(
        CommandContainer,
        repository_container=repository_container,
    )

    domain_event_container = providers.Container(
        DomainEventContainer,
        repository_container=repository_container,
    )
