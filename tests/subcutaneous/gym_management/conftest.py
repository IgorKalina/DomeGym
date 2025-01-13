import pytest

from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.gym_management.infrastructure.admin.repository.repository_memory import AdminMemoryRepository
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.infrastructure.subscription.repository.repository_memory import SubscriptionMemoryRepository
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory
from tests.common.gym_management.injection.containers.repository_memory_container import RepositoryMemoryContainer
from tests.common.gym_management.subscription.factory.subscription_db_factory import SubscriptionDBFactory


@pytest.fixture
async def di_container() -> DiContainer:
    return DiContainer(repository_container=RepositoryMemoryContainer())


@pytest.fixture
async def command_invoker(di_container: DiContainer) -> CommandInvokerMemory:
    return await di_container.command_invoker()


@pytest.fixture
async def query_invoker(di_container: DiContainer) -> QueryInvokerMemory:
    return await di_container.query_invoker()


@pytest.fixture
def admin_repository(di_container: DiContainer) -> AdminMemoryRepository:
    return di_container.repository_container.admin_repository()


@pytest.fixture
def subscription_repository(di_container: DiContainer) -> SubscriptionMemoryRepository:
    return di_container.repository_container.subscription_repository()


@pytest.fixture
async def subscription_db(subscription_repository: SubscriptionMemoryRepository) -> SubscriptionDB:
    subscription = SubscriptionDBFactory.create_subscription()
    await subscription_repository.create(subscription=subscription)
    return subscription
