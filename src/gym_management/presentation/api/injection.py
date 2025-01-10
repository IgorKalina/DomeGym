from src.gym_management import presentation
from src.gym_management.infrastructure.common.injection.containers.repository_postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer


def create_dependency_injection_container() -> DiContainer:
    di_container = DiContainer(repository_container=RepositoryPostgresContainer)
    di_container.wire(packages=[presentation])
    return di_container
