import pytest

from src.gym_management.application.admin.exceptions import AdminDoesNotExistError
from src.gym_management.application.subscription.exceptions import (
    SubscriptionDoesNotExistError,
)
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription import Subscription
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from tests.common.gym_management.admin.repository.memory import AdminMemoryRepository
from tests.common.gym_management.common import constants
from tests.common.gym_management.subscription.factory.subscription_command_factory import SubscriptionCommandFactory
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)


class TestRemoveSubscription:
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
    async def test_remove_subscription_when_subscription_exists_should_remove_subscription(
        self,
        admin_with_subscription: Admin,  # noqa: ARG002
    ) -> None:
        # Arrange
        remove_subscription_command = SubscriptionCommandFactory.create_remove_subscription_command()

        # Act
        await self._command_bus.invoke(remove_subscription_command)

        # Assert
        await self._assert_admin_has_no_subscription()

    @pytest.mark.asyncio
    async def test_remove_subscription_when_subscription_not_exists_should_fail(self) -> None:
        # Arrange
        remove_subscription_command = SubscriptionCommandFactory.create_remove_subscription_command(
            subscription_id=constants.common.NON_EXISTING_ID
        )

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._command_bus.invoke(remove_subscription_command)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_remove_subscription_when_admin_not_exists_should_fail(self, subscription: Subscription) -> None:
        # Arrange
        remove_subscription_command = SubscriptionCommandFactory.create_remove_subscription_command(
            subscription_id=subscription.id
        )

        # Act
        with pytest.raises(AdminDoesNotExistError) as err:
            await self._command_bus.invoke(remove_subscription_command)

        # Assert
        assert err.value.title == "Admin.Not_found"
        assert err.value.detail == "Admin with the provided id does not exist"
        assert err.value.error_type == ErrorType.NOT_FOUND

    async def _assert_admin_has_no_subscription(self) -> None:
        admin = await self._admin_repository.get_or_none(admin_id=constants.admin.ADMIN_ID)
        assert admin is not None
        assert admin.subscription_id is None
