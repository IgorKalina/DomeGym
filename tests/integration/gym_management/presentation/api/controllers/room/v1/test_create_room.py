from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.gym.v1.responses.gym_response import GymResponse
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.common import constants
from tests.common.gym_management.room.factory.room_request_factory import RoomRequestFactory
from tests.common.gym_management.room.service.api.v1 import RoomV1ApiService


@pytest.mark.asyncio
class TestCreateRoom:
    @pytest.fixture(autouse=True)
    def setup_method(self, room_v1_api: RoomV1ApiService) -> None:
        self._room_v1_api = room_v1_api

    async def test_when_request_valid_should_create_room(self, gym_v1: GymResponse) -> None:
        """
        Tests when subscription and gym exists for the create room request, it should create a room
        """
        # Arrange
        request = RoomRequestFactory.create_create_room_request()

        # Act
        response, response_data = await self._room_v1_api.create(
            request=request, subscription_id=gym_v1.subscription_id, gym_id=gym_v1.id
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        assert len(response_data.data) == 1
        assert len(response_data.errors) == 0
        data = response_data.data[0]
        assert data.name == request.name

    async def test_when_no_subscription_should_return_404(self) -> None:
        # Arrange
        request = RoomRequestFactory.create_create_room_request()

        # Act
        response, response_data = await self._room_v1_api.create(
            request=request,
            subscription_id=constants.common.NON_EXISTING_ID,
            gym_id=constants.common.NON_EXISTING_ID,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Subscription.Not_found"
        assert error.detail == "Subscription with the provided id not found"

    async def test_when_subscription_exists_but_gym_not_exists_should_return_404(
        self, subscription_v1: SubscriptionResponse
    ) -> None:
        # Arrange
        request = RoomRequestFactory.create_create_room_request()

        # Act
        response, response_data = await self._room_v1_api.create(
            request=request,
            subscription_id=subscription_v1.id,
            gym_id=constants.common.NON_EXISTING_ID,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Gym.Not_found"
        assert error.detail == f"Gym with the provided id not found: {constants.common.NON_EXISTING_ID}"

    async def test_when_create_room_more_than_subscription_allows_should_return_422(self, gym_v1: GymResponse) -> None:
        # Arrange
        request = RoomRequestFactory.create_create_room_request()
        for _ in range(constants.subscription.MAX_ROOMS_FREE_TIER):
            await self._room_v1_api.create(
                request=request,
                subscription_id=gym_v1.subscription_id,
                gym_id=gym_v1.id,
            )
        # No more rooms are allowed to add

        # Act
        response, response_data = await self._room_v1_api.create(
            request=request, subscription_id=gym_v1.subscription_id, gym_id=gym_v1.id
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Gym.Validation"
        assert error.detail == (
            f"A gym cannot have more rooms than the subscription allows. "
            f"Max rooms allowed: {constants.subscription.MAX_ROOMS_FREE_TIER}"
        )
