from http import HTTPStatus

import pytest

from src.gym_management.application.admins.exceptions import AdminAlreadyExistsError
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


class TestCreateSubscription:
    @pytest.fixture(autouse=True)
    def setup_method(self, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self._subscriptions_api = subscription_v1_api

    @pytest.mark.asyncio
    async def test_when_request_valid_should_create_subscription(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )

        # Act
        response, response_data = self._subscriptions_api.create(request)

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        assert response_data.status == HTTPStatus.CREATED
        _, ok_response = self._subscriptions_api.list()
        assert len(ok_response.data) == 1

    @pytest.mark.asyncio
    async def test_when_subscription_for_admin_already_exists_should_return_409(self) -> None:
        # Arrange
        request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        expected_error = AdminAlreadyExistsError()
        self._subscriptions_api.create(request)

        # Act
        response, response_data = self._subscriptions_api.create(request)

        # Assert
        assert response.status_code == HTTPStatus.CONFLICT
        assert response_data.status == HTTPStatus.CONFLICT
        assert response_data.data == []
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == expected_error.title
        assert error.detail == expected_error.detail

        _, ok_response = self._subscriptions_api.list()
        assert len(ok_response.data) == 1
