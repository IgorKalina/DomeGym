import uuid
from typing import List

import pytest

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.room.factory.room_query_factory import RoomQueryFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class TestListRooms:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        query_bus: QueryBusMemory,
        room_repository: RoomMemoryRepository,
        gym_repository: GymRepository,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self._query_bus = query_bus
        self._room_repository = room_repository
        self._gym_repository = gym_repository
        self._subscription_repository = subscription_repository

    @pytest.mark.asyncio
    async def test_list_rooms_when_exist_should_return_all_rooms(
        self, subscription: Subscription, gym: Gym, room: Room
    ) -> None:
        # Arrange
        subscription.add_gym(gym)
        await self._subscription_repository.update(subscription)
        gym.add_room(room)
        await self._gym_repository.update(gym)
        list_rooms = RoomQueryFactory.create_list_rooms_query()

        # Act
        result: List[Room] = await self._query_bus.invoke(list_rooms)

        # Assert
        assert len(result) == 1
        assert result[0] == room

    @pytest.mark.asyncio
    async def test_list_rooms_when_not_exist_should_return_empty_result(
        self, subscription: Subscription, gym: Gym
    ) -> None:  # noqa: ARG002
        # Arrange
        subscription.add_gym(gym)
        await self._subscription_repository.update(subscription)
        list_rooms = RoomQueryFactory.create_list_rooms_query()

        # Act
        result: List[Room] = await self._query_bus.invoke(list_rooms)

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_list_rooms_when_subscription_not_exists_should_fail(self, gym: Gym) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query(
            gym_id=gym.id, subscription_id=constants.common.NON_EXISTING_ID
        )

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._query_bus.invoke(list_rooms)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_list_rooms_when_gym_not_exists_should_fail(self, subscription: Subscription) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query(
            gym_id=constants.common.NON_EXISTING_ID, subscription_id=subscription.id
        )

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._query_bus.invoke(list_rooms)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == f"Gym with the provided id not found: {list_rooms.gym_id}"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_list_rooms_when_gym_not_belongs_to_subscription_should_fail(
        self, subscription: Subscription, gym: Gym
    ) -> None:
        # Arrange
        subscription.add_gym(gym)
        await self._subscription_repository.update(subscription)
        subscription_other = SubscriptionFactory.create_subscription(id=uuid.uuid4())
        await self._subscription_repository.create(subscription_other)

        list_rooms = RoomQueryFactory.create_list_rooms_query(
            gym_id=gym.id,
            subscription_id=subscription_other.id,
        )

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._query_bus.invoke(list_rooms)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == f"Gym with the provided id not found: {list_rooms.gym_id}"
        assert err.value.error_type == ErrorType.NOT_FOUND
