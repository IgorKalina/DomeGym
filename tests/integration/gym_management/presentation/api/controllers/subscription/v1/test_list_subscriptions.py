from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.subscription.service.api.v1 import SubscriptionV1ApiService


@pytest.mark.asyncio
class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(self, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self._subscriptions_api = subscription_v1_api

    async def test_when_subscriptions_exist_should_return_subscriptions(
        self,
        subscription_v1: SubscriptionResponse,
    ) -> None:
        # Arrange
        # is done via a fixture

        # Act
        response, ok_response = await self._subscriptions_api.list()

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 1
        subscription = ok_response.data[0]
        assert subscription.type == subscription_v1.type
        assert subscription.admin_id == subscription_v1.admin_id
        assert subscription.created_at == subscription_v1.created_at

    async def test_when_no_subscriptions_exist_should_return_empty_list(self) -> None:
        # Act
        response, ok_response = await self._subscriptions_api.list()

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 0
