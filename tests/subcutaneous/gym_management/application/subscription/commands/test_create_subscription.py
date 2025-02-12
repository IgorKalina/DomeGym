import pytest

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.subscription.commands.create_subscription import CreateSubscription
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from tests.common.gym_management.admin.repository.memory import AdminMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_command_factory import SubscriptionCommandFactory
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)


class TestCreateSubscription:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_bus: CommandBusMemory,
        admin_repository: AdminMemoryRepository,
        subscription_repository: SubscriptionMemoryRepository,
    ) -> None:
        self._command_bus = command_bus
        self._admin_repository = admin_repository
        self._subscription_repository = subscription_repository

    @pytest.mark.asyncio
    async def test_create_subscription_when_valid_command_should_create_subscription(self) -> None:
        # Arrange
        create_subscription_command = SubscriptionCommandFactory.create_create_subscription_command()

        # Act
        await self._command_bus.invoke(create_subscription_command)

        # Assert
        await self._assert_subscription_in_db(create_subscription_command)
        await self._assert_admin_in_db(create_subscription_command)

    @pytest.mark.asyncio
    async def test_create_subscription_when_admin_already_exists_should_fail(self) -> None:
        # Arrange
        create_subscription_command = SubscriptionCommandFactory.create_create_subscription_command()
        await self._command_bus.invoke(create_subscription_command)

        # Act
        with pytest.raises(AdminAlreadyExistsError) as err:
            await self._command_bus.invoke(create_subscription_command)

        # Assert
        assert err.value.title == "Admin.Conflict"
        assert err.value.detail == "Admin with the provided id already exists"
        assert err.value.error_type == ErrorType.CONFLICT

    async def _assert_subscription_in_db(self, create_subscription: CreateSubscription) -> None:
        subscriptions_in_db = await self._subscription_repository.get_multi()
        assert len(subscriptions_in_db) == 1
        subscription = subscriptions_in_db[0]
        assert subscription.admin_id == create_subscription.admin_id
        assert subscription.type == create_subscription.subscription_type

    async def _assert_admin_in_db(self, create_subscription: CreateSubscription) -> None:
        admin = await self._admin_repository.get_by_id(admin_id=create_subscription.admin_id)
        assert admin is not None
        subscription = await self._subscription_repository.get_by_admin_id(admin_id=create_subscription.admin_id)
        assert subscription is not None
        assert admin.subscription_id == subscription.id
