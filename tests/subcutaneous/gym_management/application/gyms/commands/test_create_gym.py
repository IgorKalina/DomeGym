import typing
import uuid
from typing import List, Optional

import pytest

from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.application.subscriptions.errors import SubscriptionDoesNotExist
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.errors import SubscriptionCannotHaveMoreGymsThanSubscriptionAllows
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from tests.common.gym_management.gym.subscription_command_factory import GymCommandFactory

if typing.TYPE_CHECKING:
    from src.shared_kernel.application.error_or import ErrorOr


class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_invoker: CommandInvokerMemory,
        subscriptions_repository: SubscriptionsRepository,
        subscription: Subscription,
    ) -> None:
        self._command_invoker = command_invoker
        self._subscriptions_repository = subscriptions_repository
        self._subscription = subscription

    @pytest.mark.asyncio
    async def test_create_gym_when_valid_command_should_create_gym(self) -> None:
        # Arrange
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)

        # Act
        result: ErrorOr[Gym] = await self._command_invoker.invoke(create_gym_command)

        # Assert
        assert result.is_ok()
        assert isinstance(result.value, Gym)
        subscription_in_db: Optional[Subscription] = await self._subscriptions_repository.get_by_id(
            subscription_id=create_gym_command.subscription_id
        )
        assert subscription_in_db is not None
        assert subscription_in_db.has_gym(gym_id=result.value.id)

    @pytest.mark.asyncio
    async def test_create_gym_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        add_gym_expected_to_succeed: List[ErrorOr[Gym]] = []
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)
        for _ in range(self._subscription.max_gyms):
            add_gym_expected_to_succeed.append(await self._command_invoker.invoke(create_gym_command))

        # Act
        add_gym_expected_to_fail: ErrorOr[Gym] = await self._command_invoker.invoke(create_gym_command)

        # Assert
        assert all(add_gym_result.is_ok() for add_gym_result in add_gym_expected_to_succeed)
        assert add_gym_expected_to_fail.is_error()
        assert add_gym_expected_to_fail.first_error == SubscriptionCannotHaveMoreGymsThanSubscriptionAllows()

    @pytest.mark.asyncio
    async def test_create_gym_when_subscription_not_exists_should_fail(self) -> None:
        # Arrange
        subscription_id_not_existing = uuid.UUID("a1111a11-12ca-4dd5-8f23-5f965a999aa9")
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=subscription_id_not_existing)

        # Act
        add_gym_result: ErrorOr[Gym] = await self._command_invoker.invoke(create_gym_command)

        # Assert
        assert add_gym_result.is_error()
        assert add_gym_result.first_error == SubscriptionDoesNotExist()
