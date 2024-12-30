import uuid
from typing import List

import pytest

from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.exceptions import SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError
from src.gym_management.infrastructure.subscription.repository.repository_memory import SubscriptionMemoryRepository
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from tests.common.gym_management.gym.factory.gym_command_factory import GymCommandFactory


class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_invoker: CommandInvokerMemory,
        subscription_repository: SubscriptionMemoryRepository,
        subscription: Subscription,
    ) -> None:
        self._command_invoker = command_invoker
        self._subscription_repository = subscription_repository
        self._subscription = subscription

    @pytest.mark.asyncio
    async def test_create_gym_when_valid_command_should_create_gym(self) -> None:
        # Arrange
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)

        # Act
        gym: Gym = await self._command_invoker.invoke(create_gym_command)

        # Assert
        assert isinstance(gym, Gym)
        subscription_in_db: Subscription | None = await self._subscription_repository.get_by_id(
            subscription_id=create_gym_command.subscription_id
        )
        assert subscription_in_db is not None
        assert subscription_in_db.has_gym(gym_id=gym.id)

    @pytest.mark.asyncio
    async def test_create_gym_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)
        created_gyms: List[Gym] = []
        for _ in range(self._subscription.max_gyms):
            created_gyms.append(await self._command_invoker.invoke(create_gym_command))

        # Act
        with pytest.raises(SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError) as err:
            await self._command_invoker.invoke(create_gym_command)

        # Assert
        assert err.value.max_gyms == self._subscription.max_gyms
        assert err.value.title == "Subscription.Validation"
        assert err.value.detail == (
            f"A subscription cannot have more gyms than the subscription allows. "
            f"Max gyms allowed: {self._subscription.max_gyms}"
        )
        assert err.value.error_type == ErrorType.VALIDATION
        assert len(created_gyms) == self._subscription.max_gyms
        assert all(isinstance(gym, Gym) for gym in created_gyms)

    @pytest.mark.asyncio
    async def test_create_gym_when_subscription_not_exists_should_fail(self) -> None:
        # Arrange
        subscription_id_not_existing = uuid.UUID("a1111a11-12ca-4dd5-8f23-5f965a999aa9")
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=subscription_id_not_existing)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._command_invoker.invoke(create_gym_command)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND
