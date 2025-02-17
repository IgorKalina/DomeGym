import pytest

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.common.dto.repository import AdminDB
from src.gym_management.domain.subscription import Subscription
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
    async def test_create_subscription_when_admin_exists_should_create_subscription(self) -> None:
        # Arrange
        create_subscription_command = SubscriptionCommandFactory.create_create_subscription_command()

        # Act
        subscription: Subscription = await self._command_bus.invoke(create_subscription_command)

        # Assert
        assert isinstance(subscription, Subscription)
        admin = await self._admin_repository.get(create_subscription_command.admin_id)
        assert admin.subscription_id == subscription.id

    @pytest.mark.asyncio
    async def test_create_subscription_when_admin_already_exists_should_fail(
        self,
        admin_with_subscription: AdminDB,  # noqa: ARG002
    ) -> None:  # noqa: ARG002
        # Arrange
        create_subscription_command = SubscriptionCommandFactory.create_create_subscription_command()

        # Act
        with pytest.raises(AdminAlreadyExistsError) as err:
            await self._command_bus.invoke(create_subscription_command)

        # Assert
        assert err.value.title == "Admin.Conflict"
        assert err.value.detail == "Admin with the provided id already exists"
        assert err.value.error_type == ErrorType.CONFLICT
