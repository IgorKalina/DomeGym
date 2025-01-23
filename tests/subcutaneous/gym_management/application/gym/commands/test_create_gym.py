import typing
from typing import List

import pytest
from freezegun import freeze_time

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.gym.commands.create_gym import CreateGym
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.exceptions import SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_command_factory import GymCommandFactory
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)

if typing.TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym


class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_invoker: CommandInvokerMemory,
        subscription_repository: SubscriptionMemoryRepository,
        gym_repository: GymMemoryRepository,
        subscription_db: SubscriptionDB,
    ) -> None:
        self._command_invoker = command_invoker
        self._subscription_repository = subscription_repository
        self._gym_repository = gym_repository

        self._subscription_db: SubscriptionDB = subscription_db
        self._subscription: Subscription = Subscription(
            id=self._subscription_db.id,
            type=self._subscription_db.type,
            admin_id=self._subscription_db.admin_id,
            created_at=subscription_db.created_at,
        )

    @pytest.mark.asyncio
    async def test_create_gym_when_valid_command_should_create_gym(self) -> None:
        # Arrange
        create_gym = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription_db.id)

        # Act
        with freeze_time(constants.common.NEW_UPDATED_AT_STR):
            gym: GymDB = await self._command_invoker.invoke(create_gym)

        # Assert
        assert isinstance(gym, GymDB)
        await self._assert_subscription_in_db(create_gym)
        await self._assert_gym_in_db(create_gym)

    @pytest.mark.asyncio
    async def test_create_gym_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        create_gym = GymCommandFactory.create_create_gym_command(subscription_id=self._subscription_db.id)
        created_gyms: List[Gym] = []
        for _ in range(self._subscription.max_gyms):
            created_gyms.append(await self._command_invoker.invoke(create_gym))

        # Act
        with pytest.raises(SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError) as err:
            await self._command_invoker.invoke(create_gym)

        # Assert
        assert err.value.max_gyms == self._subscription.max_gyms
        assert err.value.title == "Subscription.Validation"
        assert err.value.detail == (
            f"A subscription cannot have more gyms than the subscription allows. "
            f"Max gyms allowed: {self._subscription.max_gyms}"
        )
        assert err.value.error_type == ErrorType.VALIDATION
        assert len(created_gyms) == self._subscription.max_gyms
        assert all(isinstance(gym, GymDB) for gym in created_gyms)

    @pytest.mark.asyncio
    async def test_create_gym_when_subscription_not_exists_should_fail(self) -> None:
        # Arrange
        create_gym = GymCommandFactory.create_create_gym_command(subscription_id=constants.common.NON_EXISTING_ID)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._command_invoker.invoke(create_gym)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    async def _assert_subscription_in_db(self, command: CreateGym) -> None:
        subscription: SubscriptionDB | None = await self._subscription_repository.get_by_id(
            subscription_id=command.subscription_id
        )
        assert subscription is not None
        assert subscription.id == self._subscription_db.id
        assert subscription.type == self._subscription_db.type
        assert subscription.created_at == self._subscription_db.created_at  # created_at is not changed
        assert subscription.updated_at != self._subscription_db.updated_at  # updated_at is updated
        assert subscription.updated_at == constants.common.NEW_UPDATED_AT

    async def _assert_gym_in_db(self, command: CreateGym) -> None:
        gyms: List[GymDB] = await self._gym_repository.get_by_subscription_id(command.subscription_id)
        assert len(gyms) == 1
        gym = gyms[0]
        assert gym.id is not None
        assert gym.name == command.name
        assert gym.subscription_id == command.subscription_id
