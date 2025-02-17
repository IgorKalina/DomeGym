from typing import List

import pytest
from freezegun import freeze_time

from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.exceptions import SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_command_factory import GymCommandFactory
from tests.common.gym_management.subscription.repository.memory import SubscriptionMemoryRepository


class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_bus: CommandBusMemory,
        subscription_repository: SubscriptionMemoryRepository,
        subscription: Subscription,
    ) -> None:
        self._command_bus = command_bus
        self._subscription_repository = subscription_repository
        self._subscription = subscription

    @pytest.mark.asyncio
    async def test_create_gym_when_subscription_exists_should_create_gym(self) -> None:
        # Arrange
        create_gym = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)

        # Act
        with freeze_time(constants.common.NEW_UPDATED_AT):
            gym: Gym = await self._command_bus.invoke(create_gym)

        # Assert
        assert isinstance(gym, Gym)
        subscription: Subscription = await self._subscription_repository.get(self._subscription.id)
        assert subscription.has_gym(gym.id)

    @pytest.mark.asyncio
    async def test_create_gym_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        create_gym = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription.id)
        created_gyms: List[Gym] = []
        for _ in range(self._subscription.max_gyms):
            created_gyms.append(await self._command_bus.invoke(create_gym))

        # Act
        with pytest.raises(SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError) as err:
            await self._command_bus.invoke(create_gym)

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
        create_gym = GymCommandFactory.create_create_gym_command(subscription_id=constants.common.NON_EXISTING_ID)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._command_bus.invoke(create_gym)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND
