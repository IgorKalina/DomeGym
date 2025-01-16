from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


@pytest.mark.asyncio
class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(self, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self._subscriptions_api = subscription_v1_api

    async def test_when_no_subscriptions_exist_should_return_empty_list(self) -> None:
        # Act
        response, ok_response = await self._subscriptions_api.list()

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 0

    async def test_when_subscriptions_exist_should_return_subscription(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        await self._subscriptions_api.create(request)

        # Act
        response, ok_response = await self._subscriptions_api.list()

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 1
        subscription = ok_response.data[0]
        assert subscription.type == constants.subscription.DEFAULT_SUBSCRIPTION_TYPE
        assert subscription.admin_id == constants.admin.ADMIN_ID
