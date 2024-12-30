from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.gym.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management import constants
from tests.common.gym_management.gym.service.api_v1 import GymV1ApiService
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService


class TestGetGym:
    @pytest.fixture(autouse=True)
    def setup_method(self, gym_v1_api: GymV1ApiService, subscription_v1_api: SubscriptionV1ApiService) -> None:
        self.gym_v1_api = gym_v1_api
        self.subscription_v1_api = subscription_v1_api

    def test_when_subscription_and_gym_exist_should_return_200(self) -> None:
        # Arrange
        # create subscription
        create_subscription_request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        _, subscription_response = self.subscription_v1_api.create(create_subscription_request)
        expected_subscription = subscription_response.data[0]
        # create gym
        create_gym_request = CreateGymRequest(name=constants.gym.NAME)
        _, gym_response = self.gym_v1_api.create(request=create_gym_request, subscription_id=expected_subscription.id)
        expected_gym = gym_response.data[0]

        # Act
        response, response_data = self.gym_v1_api.get(gym_id=expected_gym.id, subscription_id=expected_subscription.id)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response_data.status == HTTPStatus.OK
        assert response.headers["content-type"] == "application/json"
        assert len(response_data.data) == 1
        assert len(response_data.errors) == 0
        gym_data = response_data.data[0]
        assert gym_data.id == expected_gym.id
        assert gym_data.subscription_id == expected_gym.subscription_id
        assert gym_data.name == expected_gym.name
        assert gym_data.created_at == expected_gym.created_at

    def test_when_no_subscription_should_return_404(self) -> None:
        # Act
        response, response_data = self.gym_v1_api.get(
            gym_id=constants.gym.GYM_ID, subscription_id=constants.subscription.SUBSCRIPTION_ID
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response_data.status == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Subscription.Not_found"
        assert error.detail == "Subscription with the provided id not found"

    def test_when_subscription_exists_and_no_gym_should_return_404(self) -> None:
        # Arrange
        create_subscription_request = CreateSubscriptionRequest(
            admin_id=constants.admin.ADMIN_ID,
            subscription_type=constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
        )
        self.subscription_v1_api.create(create_subscription_request)
        subscription_response = self.subscription_v1_api.get_subscription_by_admin_id(constants.admin.ADMIN_ID)

        # Act
        response, response_data = self.gym_v1_api.get(
            gym_id=constants.gym.GYM_ID, subscription_id=subscription_response.id
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response_data.status == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Gym.Not_found"
        assert error.detail == "Gym with the provided id not found"
