import uuid

import pytest

from src.gym_management.application.common.dto.repository import GymDB
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_command_factory import GymCommandFactory
from tests.common.gym_management.subscription.factory.subscription_db_factory import SubscriptionDBFactory


class TestGetGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_bus: CommandBusMemory,
        query_bus: QueryBusMemory,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._subscription_repository = subscription_repository

    @pytest.mark.asyncio
    async def test_get_gym_when_gym_and_subscription_exist_should_return_gym(
        self, subscription_db: Subscription
    ) -> None:
        # Arrange
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=subscription_db.id)
        expected_gym: GymDB = await self._command_bus.invoke(create_gym_command)
        get_gym: GetGym = GetGym(subscription_id=constants.subscription.SUBSCRIPTION_ID, gym_id=expected_gym.id)

        # Act
        gym: GymDB = await self._query_bus.invoke(get_gym)

        # Assert
        assert gym == expected_gym

    @pytest.mark.asyncio
    async def test_get_gym_when_subscription_not_exist_should_raise_exception(self) -> None:
        # Arrange
        get_gym: GetGym = GetGym(subscription_id=constants.subscription.SUBSCRIPTION_ID, gym_id=constants.gym.GYM_ID)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._query_bus.invoke(get_gym)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_gym_when_subscription_exists_and_no_gym_should_raise_exception(
        self, subscription_db: Subscription
    ) -> None:
        # Arrange
        get_gym: GetGym = GetGym(subscription_id=subscription_db.id, gym_id=constants.gym.GYM_ID)

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._query_bus.invoke(get_gym)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_gym_when_gym_not_belongs_to_subscription_should_raise_exception(self, gym_db: GymDB) -> None:
        # Arrange
        subscription_other = SubscriptionDBFactory.create_subscription(id=uuid.uuid4())
        await self._subscription_repository.create(subscription_other)

        get_gym: GetGym = GetGym(subscription_id=subscription_other.id, gym_id=gym_db.id)

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._query_bus.invoke(get_gym)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND
