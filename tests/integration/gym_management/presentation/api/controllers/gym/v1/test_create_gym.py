from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.gym.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_request_factory import GymRequestFactory
from tests.common.gym_management.gym.service.api.v1 import GymV1ApiService


@pytest.mark.asyncio
class TestCreateGym:
    @pytest.fixture(autouse=True)
    def setup_method(self, gym_v1_api: GymV1ApiService) -> None:
        self._gym_v1_api = gym_v1_api

    async def test_when_subscription_exists_should_create_gym(self, subscription_v1: SubscriptionResponse) -> None:
        # Arrange
        request: CreateGymRequest = GymRequestFactory.create_create_gym_request()

        # Act
        response, response_data = await self._gym_v1_api.create(request=request, subscription_id=subscription_v1.id)

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        assert len(response_data.data) == 1
        assert len(response_data.errors) == 0
        data = response_data.data[0]
        assert data.name == request.name

    async def test_when_no_subscription_should_return_404(self) -> None:
        # Arrange
        request = CreateGymRequest(name=constants.gym.NAME)

        # Act
        response, response_data = await self._gym_v1_api.create(
            request=request, subscription_id=constants.common.NON_EXISTING_ID
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Subscription.Not_found"
        assert error.detail == "Subscription with the provided id not found"
