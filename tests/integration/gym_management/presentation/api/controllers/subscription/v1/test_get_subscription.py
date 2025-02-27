from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.common import constants
from tests.common.gym_management.subscription.service.api.v1 import SubscriptionV1ApiService


class TestGetSubscription:
    @pytest.fixture(autouse=True)
    def setup_method(self, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self._subscriptions_api = subscription_v1_api

    @pytest.mark.asyncio
    async def test_when_subscription_not_exists_should_return_404(self) -> None:
        # Act
        response, response_data = await self._subscriptions_api.get(subscription_id=constants.common.NON_EXISTING_ID)

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Subscription.Not_found"
        assert error.detail == "Subscription with the provided id not found"

    @pytest.mark.asyncio
    async def test_when_subscription_exists_should_return_subscription(
        self, subscription_v1: SubscriptionResponse
    ) -> None:
        # Act
        response, response_data = await self._subscriptions_api.delete(subscription_id=subscription_v1.id)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.headers["content-type"] == "application/json"
        assert len(response_data.data) == 1
        assert len(response_data.errors) == 0
        data = response_data.data[0]
        assert data == subscription_v1
