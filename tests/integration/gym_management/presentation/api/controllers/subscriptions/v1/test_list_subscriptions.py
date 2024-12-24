from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


class TestListSubscriptions:
    @pytest.fixture(autouse=True)
    def setup_method(self, api_client: TestClient) -> None:
        self._api_client = api_client
        self._subscriptions_api = SubscriptionV1ApiService(self._api_client)

    @pytest.mark.asyncio
    async def test_when_no_subscriptions_exist_should_return_empty_list(self) -> None:
        # Act
        response, ok_response = self._subscriptions_api.list()

        # Assert
        assert response.status_code == HTTPStatus.OK
        _, ok_response = self._subscriptions_api.list()
        assert len(ok_response.data) == 0

    @pytest.mark.asyncio
    async def test_when_subscriptions_exist_should_return_subscription(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        self._subscriptions_api.create(request)

        # Act
        response, ok_response = self._subscriptions_api.list()

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 1
        subscription = ok_response.data[0]
        assert subscription.type == constants.subscription.DEFAULT_SUBSCRIPTION_TYPE
        assert subscription.admin_id == constants.admin.ADMIN_ID
