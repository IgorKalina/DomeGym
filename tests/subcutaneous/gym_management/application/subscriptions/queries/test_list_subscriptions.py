import typing
from typing import List

import pytest

from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.shared_kernel.application.mediator.interfaces import IMediator
from tests.common.gym_management.subscription.subscription_factory import SubscriptionFactory
from tests.common.gym_management.subscription.subscription_query_factory import SubscriptionQueryFactory

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        mediator: IMediator,
        subscriptions_repository: SubscriptionsRepository,
    ) -> None:
        self._mediator = mediator
        self._subscriptions_repository = subscriptions_repository

    @pytest.mark.asyncio
    async def test_list_subscriptions_when_exists_should_return_all_subscriptions(self) -> None:
        subscription = SubscriptionFactory.create_subscription()
        await self._subscriptions_repository.create(subscription)
        query = SubscriptionQueryFactory.create_list_subscription_query()

        result: List[Subscription] = await self._mediator.query(query)

        assert len(result) == 1
        assert result[0] == subscription

    @pytest.mark.asyncio
    async def test_list_subscriptions_when_not_exists_should_return_empty_result(self) -> None:
        query = SubscriptionQueryFactory.create_list_subscription_query()

        result: List[Subscription] = await self._mediator.query(query)

        assert result == []
