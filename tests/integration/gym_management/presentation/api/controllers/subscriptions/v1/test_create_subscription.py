from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


class TestCreateSubscription:
    @pytest.fixture(autouse=True)
    def setup_method(self, api_client: TestClient) -> None:
        self._api_client = api_client
        self._subscriptions_api = SubscriptionV1ApiService(self._api_client)

    @pytest.mark.asyncio
    async def test_when_request_valid_should_create_subscription(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )

        # Act
        response, ok_response = self._subscriptions_api.create(request)

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        _, ok_response = self._subscriptions_api.list()
        assert len(ok_response.data) == 1

    @pytest.mark.asyncio
    async def test_when_subscription_for_admin_already_exists_should_return_409(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        self._subscriptions_api.create(request)

        # Act
        response, ok_response = self._subscriptions_api.create(request)

        # Assert
        assert response.status_code == HTTPStatus.CONFLICT
        _, ok_response = self._subscriptions_api.list()
        assert len(ok_response.data) == 1
