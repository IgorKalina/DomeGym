import pytest
from dependency_injector import containers

from src.common.mediator.interfaces import IMediator
from src.gym_management.application.common.interfaces.persistence.admins_repository import AdminsRepository
from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.presentation.api.dependency_injection import DependencyContainer


@pytest.fixture(scope="session")
def di_container() -> containers.DeclarativeContainer:
    container = DependencyContainer()
    yield container


@pytest.fixture(scope="session")
def mediator(di_container) -> IMediator:
    return di_container.app.mediator.mediator()


@pytest.fixture(scope="session")
def admins_repository(di_container) -> AdminsRepository:
    return di_container.infrastructure.admins_repository()


@pytest.fixture(scope="session")
def subscriptions_repository(di_container) -> SubscriptionsRepository:
    return di_container.infrastructure.subscriptions_repository()
