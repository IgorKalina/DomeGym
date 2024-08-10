from typing import List

import pytest

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.mediator.interfaces import IMediator
from tests.common.subscription.subscription_factory import SubscriptionFactory
from tests.common.subscription.subscription_query_factory import SubscriptionQueryFactory


class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        *args,
        mediator: IMediator,
        subscriptions_repository: SubscriptionsRepository,
        **kwargs,
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
