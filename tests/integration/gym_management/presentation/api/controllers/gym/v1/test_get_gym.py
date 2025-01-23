from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.gym.v1.responses.gym_response import GymResponse
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.service.api.v1 import GymV1ApiService


@pytest.mark.asyncio
class TestGetGym:
    @pytest.fixture(autouse=True)
    def setup_method(self, gym_v1_api: GymV1ApiService) -> None:
        self._gym_v1_api = gym_v1_api

    async def test_when_subscription_and_gym_exist_should_return_200(self, gym_v1: GymResponse) -> None:
        # Arrange
        # is done via a fixture

        # Act
        response, response_data = await self._gym_v1_api.get(gym_id=gym_v1.id, subscription_id=gym_v1.subscription_id)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response_data.status == HTTPStatus.OK
        assert response.headers["content-type"] == "application/json"
        assert len(response_data.data) == 1
        assert len(response_data.errors) == 0
        gym_data = response_data.data[0]
        assert gym_data.id == gym_v1.id
        assert gym_data.subscription_id == gym_v1.subscription_id
        assert gym_data.name == gym_v1.name
        assert gym_data.created_at == gym_v1.created_at

    async def test_when_no_subscription_should_return_404(self) -> None:
        # Act
        response, response_data = await self._gym_v1_api.get(
            gym_id=constants.gym.GYM_ID, subscription_id=constants.subscription.SUBSCRIPTION_ID
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Subscription.Not_found"
        assert error.detail == "Subscription with the provided id not found"

    async def test_when_subscription_exists_and_no_gym_should_return_404(
        self, subscription_v1: SubscriptionResponse
    ) -> None:
        # Arrange
        # is done via a fixture

        # Act
        response, response_data = await self._gym_v1_api.get(
            gym_id=constants.common.NON_EXISTING_ID, subscription_id=subscription_v1.id
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Gym.Not_found"
        assert error.detail == "Gym with the provided id not found"
