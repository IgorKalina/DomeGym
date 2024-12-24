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
from tests.common.gym_management.gym.service.api_v1 import GymV1ApiService
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


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
    api.container.override(di_container)  # type: ignore
    return TestClient(app=api)


# todo: move to a separate conftest file
@pytest.fixture
def subscription_v1_api(api_client: TestClient) -> SubscriptionV1ApiService:
    return SubscriptionV1ApiService(api_client)


@pytest.fixture
def gym_v1_api(api_client: TestClient) -> GymV1ApiService:
    return GymV1ApiService(api_client)
