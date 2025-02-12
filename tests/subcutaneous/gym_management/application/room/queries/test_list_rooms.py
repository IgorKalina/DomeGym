import typing
import uuid
from typing import List

import pytest

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.shared_kernel.application.error_or import ErrorType
from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.room.factory.room_db_factory import RoomDBFactory
from tests.common.gym_management.room.factory.room_query_factory import RoomQueryFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_db_factory import SubscriptionDBFactory

if typing.TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.room import RoomDB


class TestListRooms:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        query_bus: QueryBusMemory,
        room_repository: RoomMemoryRepository,
        subscription_repository: SubscriptionRepository,
        gym_db: GymDB,
    ) -> None:
        self._query_bus = query_bus
        self._room_repository = room_repository
        self._subscription_repository = subscription_repository

        self._gym_db = gym_db

    @pytest.mark.asyncio
    async def test_list_rooms_when_exist_should_return_all_subscriptions(self) -> None:
        # Arrange
        room: RoomDB = RoomDBFactory.create_room(gym_id=self._gym_db.id, subscription_id=self._gym_db.subscription_id)
        await self._room_repository.create(room)
        list_rooms = RoomQueryFactory.create_list_rooms_query()

        # Act
        result: List[RoomDB] = await self._query_bus.invoke(list_rooms)

        # Assert
        assert len(result) == 1
        assert result[0] == room

    @pytest.mark.asyncio
    async def test_list_rooms_when_not_exist_should_return_empty_result(self) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query()

        # Act
        result: List[RoomDB] = await self._query_bus.invoke(list_rooms)

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_list_rooms_when_subscription_not_exists_should_raise_exception(self) -> None:
        # Arrange
        list_rooms = RoomQueryFactory.create_list_rooms_query(subscription_id=constants.common.NON_EXISTING_ID)

        # Act
        with pytest.raises(SubscriptionDoesNotExistError) as err:
            await self._query_bus.invoke(list_rooms)

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
            await self._query_bus.invoke(list_rooms)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND

    @pytest.mark.asyncio
    async def test_list_rooms_when_gym_not_belongs_to_subscription_should_raise_exception(self, gym_db: GymDB) -> None:
        # Arrange
        subscription_other = SubscriptionDBFactory.create_subscription(id=uuid.uuid4())
        await self._subscription_repository.create(subscription_other)

        list_rooms = RoomQueryFactory.create_list_rooms_query(
            gym_id=gym_db.id,
            subscription_id=subscription_other.id,
        )

        # Act
        with pytest.raises(GymDoesNotExistError) as err:
            await self._query_bus.invoke(list_rooms)

        # Assert
        assert err.value.title == "Gym.Not_found"
        assert err.value.detail == "Gym with the provided id not found"
        assert err.value.error_type == ErrorType.NOT_FOUND
