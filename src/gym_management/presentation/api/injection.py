from src.gym_management import presentation
from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.common.injection.containers.repository_postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer


def create_dependency_injection_container() -> DiContainer:
    di_container = DiContainer(repository_container=RepositoryPostgresContainer(config=load_config()))
    di_container.wire(packages=[presentation])
    return di_container
