from src.gym_management import presentation
from src.gym_management.infrastructure.config import load_config
from src.gym_management.infrastructure.injection.containers.eventbus.rabbitmq import EventbusRabbitmqContainer
from src.gym_management.infrastructure.injection.containers.repository.postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.injection.main import DiContainer


def create_dependency_injection_container() -> DiContainer:
    config = load_config()
    repository_container = RepositoryPostgresContainer(config=config.database)
    eventbus_container = EventbusRabbitmqContainer(config=config.rabbitmq)
    di_container = DiContainer(
        repository_container=repository_container,
        eventbus_container=eventbus_container,
    )
    di_container.wire(packages=[presentation])
    return di_container
