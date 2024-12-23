import pytest
from fastapi.testclient import TestClient

from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.infrastructure.admins.repository.repository_memory import AdminsMemoryRepository
from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.api import init_api
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory


@pytest.fixture
def di_container() -> DiContainer:
    return DiContainer()


@pytest.fixture
def command_invoker(di_container: DiContainer) -> CommandInvokerMemory:
    return di_container.command_invoker()


@pytest.fixture
def query_invoker(di_container: DiContainer) -> QueryInvokerMemory:
    return di_container.query_invoker()


@pytest.fixture
def admins_repository(di_container: DiContainer) -> AdminsMemoryRepository:
    return di_container.repositories.admins_repository()


@pytest.fixture
def subscriptions_repository(di_container: DiContainer) -> SubscriptionsRepository:
    return di_container.repositories.subscriptions_repository()


@pytest.fixture
def api_client(di_container: DiContainer) -> TestClient:
    api = init_api(config=load_config().api)
    api.container.override(di_container)
    return TestClient(app=api)
