import typing
from typing import List

import pytest

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.room.factory.room_db_factory import RoomDBFactory
from tests.common.gym_management.room.factory.room_query_factory import RoomQueryFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository

if typing.TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.room import RoomDB


class TestListRooms:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        query_invoker: QueryInvokerMemory,
        room_repository: RoomMemoryRepository,
        gym_db: GymDB,
    ) -> None:
        self._query_invoker = query_invoker
        self._room_repository = room_repository

        self._gym_db = gym_db

    @pytest.mark.asyncio
    async def test_list_rooms_when_exist_should_return_all_subscriptions(self) -> None:
        # Arrange
        room: RoomDB = RoomDBFactory.create_room(gym_id=self._gym_db.id, subscription_id=self._gym_db.subscription_id)
        await self._room_repository.create(room)
        list_rooms = RoomQueryFactory.create_list_rooms_query()

        # Act
        result: List[RoomDB] = await self._query_invoker.invoke(list_rooms)

        # Assert
        assert len(result) == 1
        assert result[0] == room

    @pytest.mark.asyncio
    async def test_list_rooms_when_not_exist_should_return_empty_result(self) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query()

        # Act
        result: List[RoomDB] = await self._query_invoker.invoke(list_rooms)

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_list_rooms_when_subscription_not_exists_should_raise_exception(self) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query(subscription_id=constants.common.NON_EXISTING_ID)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._query_invoker.invoke(list_rooms)

        # Assert
        assert err.value.title == "Subscription.Not_found"
        assert err.value.detail == "Subscription with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_list_rooms_when_gym_not_exists_should_raise_exception(self) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query(gym_id=constants.common.NON_EXISTING_ID)

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._query_invoker.invoke(list_rooms)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND
