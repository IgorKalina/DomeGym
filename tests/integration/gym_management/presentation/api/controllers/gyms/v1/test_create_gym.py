from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.gyms.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants
from tests.common.gym_management.gym.service.api_v1 import GymV1ApiService
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(self, gym_v1_api: GymV1ApiService, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self._gym_v1_api = gym_v1_api
        self._subscription_v1_api = subscription_v1_api

    def test_when_no_subscription_should_return_404(self) -> None:
        # Arrange
        request = CreateGymRequest(name=constants.gym.NAME)

        # Act
        response, response_data = self._gym_v1_api.create(
            request=request, subscription_id=constants.subscription.SUBSCRIPTION_ID
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response_data.status == HTTPStatus.NOT_FOUND

    def test_when_subscription_exists_should_create_gym(self) -> None:
        # Arrange
        create_gym_request = CreateGymRequest(name=constants.gym.NAME)
        create_subscription_request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        self._subscription_v1_api.create(create_subscription_request)
        subscription_response = self._subscription_v1_api.get_subscription_by_admin_id(constants.admin.ADMIN_ID)

        # Act
        response, response_data = self._gym_v1_api.create(
            request=create_gym_request, subscription_id=subscription_response.id
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        assert response_data.status == HTTPStatus.CREATED
