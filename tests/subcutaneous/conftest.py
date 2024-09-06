from typing import Generator

import pytest
from dependency_injector import containers, providers

from src.gym_management.application.common.interfaces.persistence.admins_repository import AdminsRepository
from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.dependency_injection import ApplicationContainer
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.presentation.api.dependency_injection import DependencyContainer
from src.shared_kernel.mediator.interfaces import IMediator
from tests.common.containers.infrastructure import InfrastructureTestContainer
from tests.common.subscription.factories.subscription_factory import SubscriptionFactory


@pytest.fixture
def di_container() -> Generator[containers.DeclarativeContainer, None, None]:
    di_container = DependencyContainer()
    di_container.infrastructure.override(providers.Container(InfrastructureTestContainer))
    yield di_container


@pytest.fixture
async def mediator(di_container) -> IMediator:
    mediator = await di_container.app.mediator()
    return mediator


@pytest.fixture
def admins_repository(di_container) -> AdminsRepository:
    return di_container.infrastructure.admins_repository()


@pytest.fixture
def subscriptions_repository(di_container) -> SubscriptionsRepository:
    return di_container.infrastructure.subscriptions_repository()


@pytest.fixture
async def subscription(subscriptions_repository: SubscriptionsRepository) -> Subscription:
    subscription = SubscriptionFactory.create_subscription()
    await subscriptions_repository.create(subscription=subscription)
    return subscription
