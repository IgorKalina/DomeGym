import typing

import pytest

from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory
from tests.common.gym_management import constants
from tests.common.gym_management.gym.factory.gym_command_factory import GymCommandFactory

if typing.TYPE_CHECKING:
    from src.gym_management.application.gym.dto.repository import GymDB


class TestGetGym:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        command_invoker: CommandInvokerMemory,
        query_invoker: QueryInvokerMemory,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self._command_invoker = command_invoker
        self._query_invoker = query_invoker
        self._subscription_repository = subscription_repository

    @pytest.mark.asyncio
    async def test_get_gym_when_gym_and_subscription_exist_should_return_gym(
        self, subscription_db: Subscription
    ) -> None:
        # Arrange
        create_gym_command = GymCommandFactory.create_create_gym_command(subscription_id=subscription_db.id)
        expected_gym: GymDB = await self._command_invoker.invoke(create_gym_command)
        get_gym: GetGym = GetGym(subscription_id=constants.subscription.SUBSCRIPTION_ID, gym_id=expected_gym.id)

        # Act
        gym: GymDB = await self._query_invoker.invoke(get_gym)

        # Assert
        assert gym == expected_gym

    @pytest.mark.asyncio
    async def test_get_gym_when_subscription_not_exist_should_raise_exception(self) -> None:
        # Arrange
        get_gym: GetGym = GetGym(subscription_id=constants.subscription.SUBSCRIPTION_ID, gym_id=constants.gym.GYM_ID)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._query_invoker.invoke(get_gym)

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
            await self._query_invoker.invoke(get_gym)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND
