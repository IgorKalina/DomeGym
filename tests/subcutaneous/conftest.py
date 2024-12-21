import pytest
from dependency_injector import containers

from src.gym_management.application.common.interfaces.repository.admins_repository import AdminsRepository
from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.presentation.api.dependency_injection import DependencyContainer
from src.shared_kernel.application.mediator.interfaces import IMediator
from tests.common.gym_management.subscription.subscription_factory import SubscriptionFactory


@pytest.fixture
def di_container() -> containers.DeclarativeContainer:
    return DependencyContainer()


@pytest.fixture
def mediator(di_container: containers.DeclarativeContainer) -> IMediator:
    return di_container.app.mediator.mediator()


@pytest.fixture
def admins_repository(di_container: containers.DeclarativeContainer) -> AdminsRepository:
    return di_container.infrastructure.admins_repository()


@pytest.fixture
def subscriptions_repository(di_container: containers.DeclarativeContainer) -> SubscriptionsRepository:
    return di_container.infrastructure.subscriptions_repository()


@pytest.fixture
async def subscription(subscriptions_repository: SubscriptionsRepository) -> Subscription:
    subscription = SubscriptionFactory.create_subscription()
    await subscriptions_repository.create(subscription=subscription)
    return subscription
