from http import HTTPStatus

import pytest

from src.gym_management.presentation.api.controllers.gym.v1.responses.gym_response import GymResponse
from src.gym_management.presentation.api.controllers.room.v1.responses.room_response import RoomResponse
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.common import constants
from tests.common.gym_management.room.service.api.v1 import RoomV1ApiService


@pytest.mark.asyncio
class TestListRooms:
    @pytest.fixture(autouse=True)
    def setup_method(self, room_v1_api: RoomV1ApiService) -> None:
        self._room_v1_api = room_v1_api

    async def test_when_rooms_exist_should_return_200(
        self,
        room_v1: RoomResponse,
    ) -> None:
        # Arrange
        # is done via a fixture

        # Act
        response, ok_response = await self._room_v1_api.list(
            gym_id=room_v1.gym_id,
            subscription_id=room_v1.subscription_id,
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 1
        room: RoomResponse = ok_response.data[0]
        assert room.id == room_v1.id
        assert room.gym_id == room_v1.gym_id
        assert room.created_at == room_v1.created_at

    async def test_when_no_rooms_exist_should_return_200(self, gym_v1: GymResponse) -> None:
        # Arrange
        # is done via a fixture

        # Act
        response, ok_response = await self._room_v1_api.list(
            gym_id=gym_v1.id,
            subscription_id=gym_v1.subscription_id,
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert len(ok_response.data) == 0

    async def test_when_subscription_not_exists_should_return_404(self) -> None:
        # Arrange
        # is done via a fixture

        # Act
        response, response_data = await self._room_v1_api.list(
            gym_id=constants.common.NON_EXISTING_ID,
            subscription_id=constants.common.NON_EXISTING_ID,
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
        # is done via a fixture

        # Act
        response, response_data = await self._room_v1_api.list(
            gym_id=constants.common.NON_EXISTING_ID,
            subscription_id=subscription_v1.id,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.headers["content-type"] == "application/problem+json"
        assert len(response_data.data) == 0
        assert len(response_data.errors) == 1
        error = response_data.errors[0]
        assert error.title == "Gym.Not_found"
        assert error.detail == "Gym with the provided id not found"
