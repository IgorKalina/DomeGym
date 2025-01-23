from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management.common import constants
from tests.common.gym_management.subscription.factory.subscription_request_factory import SubscriptionRequestFactory
from tests.common.gym_management.subscription.service.api.v1 import SubscriptionV1ApiService


class TestCreateSubscription:
    @pytest.fixture(autouse=True)
    def setup_method(self, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self._subscriptions_api = subscription_v1_api

    @pytest.mark.asyncio
    async def test_when_request_valid_should_create_subscription(self) -> None:
        # Arrange
        request = SubscriptionRequestFactory.create_create_subscription_request()

        # Act
        response, response_data = await self._subscriptions_api.create(request)

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        assert response.headers["content-type"] == "application/json"
        assert len(response_data.data) == 1
        assert len(response_data.errors) == 0
        data = response_data.data[0]
        assert data.admin_id == constants.admin.ADMIN_ID
        assert data.type == constants.subscription.DEFAULT_SUBSCRIPTION_TYPE

    @pytest.mark.asyncio
    async def test_when_subscription_for_admin_already_exists_should_return_409(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        await self._subscriptions_api.create(request)

        # Act
        response, response_data = await self._subscriptions_api.create(request)

        # Assert
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Admin.Conflict"
        assert error.detail == "Admin with the provided id already exists"

        _, ok_response = await self._subscriptions_api.list()
        assert len(ok_response.data) == 1
