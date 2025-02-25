from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.config import Config
from src.gym_management.infrastructure.common.injection.containers.command import CommandContainer
from src.gym_management.infrastructure.common.injection.containers.domain_event import DomainEventContainer
from src.gym_management.infrastructure.common.injection.containers.eventbus.base import EventbusContainer
from src.gym_management.infrastructure.common.injection.containers.query import QueryContainer
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer


class DiContainer(containers.DeclarativeContainer):
    # dependencies
    config: providers.Dependency[Config] = providers.Dependency(instance_of=Config)
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    eventbus_container: EventbusContainer = providers.DependenciesContainer()

    # containers
    query_container = providers.Container(
        QueryContainer,
        repository_container=repository_container,
    )
    command_container = providers.Container(
        CommandContainer,
        repository_container=repository_container,
    )

    domain_event_container = providers.Container(
        DomainEventContainer,
        repository_container=repository_container,
    )
