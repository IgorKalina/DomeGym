import pytest

from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.admins.repository.repository_memory import AdminsMemoryRepository
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
def admins_repository(di_container: DiContainer) -> AdminsMemoryRepository:
    return di_container.repositories.admins_repository()


@pytest.fixture
def subscriptions_repository(di_container: DiContainer) -> SubscriptionsRepository:
    return di_container.repositories.subscriptions_repository()


@pytest.fixture
async def subscription(subscriptions_repository: SubscriptionsRepository) -> Subscription:
    subscription = SubscriptionFactory.create_subscription()
    await subscriptions_repository.create(subscription=subscription)
    return subscription
