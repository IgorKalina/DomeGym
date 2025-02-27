from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.common.injection.containers.command import CommandContainer
from src.gym_management.infrastructure.common.injection.containers.domain_event import DomainEventContainer
from src.gym_management.infrastructure.common.injection.containers.eventbus.base import EventbusContainer
from src.gym_management.infrastructure.common.injection.containers.eventbus.rabbitmq import EventbusRabbitmqContainer
from src.gym_management.infrastructure.common.injection.containers.query import QueryContainer
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.gym_management.infrastructure.common.injection.containers.repository.postgres import (
    RepositoryPostgresContainer,
)


class DiContainer(containers.DeclarativeContainer):
    config = providers.Callable(load_config)
    repository_container: RepositoryContainer = providers.Container(
        RepositoryPostgresContainer, config=config.provided.database
    )
    eventbus_container: EventbusContainer = providers.Container(
        EventbusRabbitmqContainer, config=config.provided.rabbitmq
    )

    # containers
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
