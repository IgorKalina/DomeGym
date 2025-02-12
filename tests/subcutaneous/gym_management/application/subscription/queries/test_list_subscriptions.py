import typing
from typing import List

import pytest

from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory
from tests.common.gym_management.subscription.factory.subscription_db_factory import SubscriptionDBFactory
from tests.common.gym_management.subscription.factory.subscription_query_factory import SubscriptionQueryFactory
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        query_bus: QueryBusMemory,
        subscription_repository: SubscriptionMemoryRepository,
    ) -> None:
        self._query_bus = query_bus
        self._subscription_repository = subscription_repository

    @pytest.mark.asyncio
    async def test_list_subscriptions_when_exist_should_return_all_subscriptions(self) -> None:
        # Arrange
        subscription = SubscriptionDBFactory.create_subscription()
        await self._subscription_repository.create(subscription)
        query = SubscriptionQueryFactory.create_list_subscription_query()

        # Act
        result: List[Subscription] = await self._query_bus.invoke(query)

        # Assert
        assert len(result) == 1
        assert result[0] == subscription

    @pytest.mark.asyncio
    async def test_list_subscriptions_when_not_exist_should_return_empty_result(self) -> None:
        # Arrange
        query = SubscriptionQueryFactory.create_list_subscription_query()

        # Act
        result: List[Subscription] = await self._query_bus.invoke(query)

        # Assert
        assert result == []
