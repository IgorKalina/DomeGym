import typing
from typing import List

import pytest

from src.gym_management.infrastructure.common.postgres.repository.subscription.repository_memory import (
    SubscriptionMemoryRepository,
)
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory
from tests.common.gym_management.subscription.factory.subscription_db_factory import SubscriptionDBFactory
from tests.common.gym_management.subscription.factory.subscription_query_factory import SubscriptionQueryFactory

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        query_invoker: QueryInvokerMemory,
        subscription_repository: SubscriptionMemoryRepository,
    ) -> None:
        self._query_invoker = query_invoker
        self._subscription_repository = subscription_repository

    @pytest.mark.asyncio
    async def test_list_subscriptions_when_exists_should_return_all_subscriptions(self) -> None:
        # Arrange
        subscription = SubscriptionDBFactory.create_subscription()
        await self._subscription_repository.create(subscription)
        query = SubscriptionQueryFactory.create_list_subscription_query()

        # Act
        result: List[Subscription] = await self._query_invoker.invoke(query)

        # Assert
        assert len(result) == 1
        assert result[0] == subscription

    @pytest.mark.asyncio
    async def test_list_subscriptions_when_not_exists_should_return_empty_result(self) -> None:
        # Arrange
        query = SubscriptionQueryFactory.create_list_subscription_query()

        # Act
        result: List[Subscription] = await self._query_invoker.invoke(query)

        # Assert
        assert result == []
