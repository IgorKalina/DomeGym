import uuid
from typing import List, Optional

import pytest

from src.common.error_or import ErrorOr
from src.common.mediator.interfaces import IMediator
from src.gym_management.application.common.interfaces.persistence.admins_repository import AdminsRepository
from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.subscriptions.errors import SubscriptionDoesNotExist
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.errors import SubscriptionCannotHaveMoreGymsThanSubscriptionAllows
from tests.common.gym.subscription_command_factory import GymCommandFactory


class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        *args,
        mediator: IMediator,
        admins_repository: AdminsRepository,
        subscriptions_repository: SubscriptionsRepository,
        subscription: Subscription,
        **kwargs,
    ) -> None:
        self._mediator = mediator
        self._subscriptions_repository = subscriptions_repository
        self._subscription = subscription

    @pytest.mark.asyncio
    async def test_create_gym_when_valid_command_should_create_gym(self) -> None:
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)

        result: ErrorOr[Gym] = await self._mediator.send(create_gym_command)

        assert result.is_ok()
        assert isinstance(result.value, Gym)
        subscription_in_db: Optional[Subscription] = await self._subscriptions_repository.get_by_id(
            subscription_id=create_gym_command.subscription_id
        )
        assert subscription_in_db is not None
        assert subscription_in_db.has_gym(gym_id=result.value.id)

    @pytest.mark.asyncio
    async def test_create_gym_when_more_than_subscription_allows_should_fail(self) -> None:
        add_gym_expected_to_succeed: List[ErrorOr[Gym]] = []
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)
        for _ in range(self._subscription.max_gyms):
            add_gym_expected_to_succeed.append(await self._mediator.send(create_gym_command))

        add_gym_expected_to_fail: ErrorOr[Gym] = await self._mediator.send(create_gym_command)

        assert all(add_gym_result.is_ok() for add_gym_result in add_gym_expected_to_succeed)
        assert add_gym_expected_to_fail.is_error()
        assert add_gym_expected_to_fail.first_error == SubscriptionCannotHaveMoreGymsThanSubscriptionAllows()

    @pytest.mark.asyncio
    async def test_create_gym_when_subscription_not_exists_should_fail(self) -> None:
        subscription_id_not_existing = uuid.UUID("a1111a11-12ca-4dd5-8f23-5f965a999aa9")
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=subscription_id_not_existing)

        add_gym_result: ErrorOr[Gym] = await self._mediator.send(create_gym_command)

        assert add_gym_result.is_error()
        assert add_gym_result.first_error == SubscriptionDoesNotExist()
