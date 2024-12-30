import pytest

from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.admin.repository.repository_memory import AdminMemoryRepository
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


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
def admin_repository(di_container: DiContainer) -> AdminMemoryRepository:
    return di_container.repositories.admin_repository()


@pytest.fixture
def subscription_repository(di_container: DiContainer) -> SubscriptionRepository:
    return di_container.repositories.subscription_repository()


@pytest.fixture
async def subscription(subscription_repository: SubscriptionRepository) -> Subscription:
    subscription = SubscriptionFactory.create_subscription()
    await subscription_repository.create(subscription=subscription)
    return subscription
